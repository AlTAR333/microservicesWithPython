# activity-service — Module 3: Synchronous Communication
#
# This file wires the FastAPI app together and contains the two outbound
# HTTP helpers you must implement (see YOUR TASK below).
#
# To run:
#   uvicorn app.main:app --reload --port 8003

import httpx
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from app.rabbitmq_publisher import publish_message
from app.infrastructure.auth_client import get_auth_headers
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from app.config import settings
from app.database import Base, engine, get_db
from app import repository, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="activity-service")


# ---------------------------------------------------------------------------
# YOUR TASK — implement the two functions below
# ---------------------------------------------------------------------------

@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    retry=retry_if_exception_type(httpx.RequestError),
    reraise=True
)
async def validate_user(user_id: str) -> None:
    """
    Verify that the user exists in user-service before logging an activity.

    Call: GET {settings.user_service_url}/v1/users/{user_id}

    Behaviour:
    - 200  → user exists, return normally (None)
    - 404  → raise HTTPException(status_code=404, detail="User not found")
    - Network error (httpx.RequestError) → retry the call once, then raise
             HTTPException(status_code=503, detail="user-service unavailable")
    - Any other non-2xx status → raise HTTPException(status_code=503, ...)

    Use `async with httpx.AsyncClient(timeout=5.0) as client:` for HTTP calls.
    This call is CRITICAL — the request must not proceed if validation fails.
    """
    url = f"{settings.user_service_url}/v1/users/{user_id}"
    try:
        headers = await get_auth_headers()
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get(url, headers=headers)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")    
        response.raise_for_status() 
    except httpx.HTTPStatusError as e:
        if e.response.status_code >= 500:
            raise httpx.RequestError("User service returned a server error") from e
        raise


async def fetch_game(game_id: str) -> dict | None:
    """
    Fetch game data from game-service to enrich the activity response.

    Call: GET {settings.game_service_url}/v1/games/{game_id}

    Behaviour:
    - 200  → return the response JSON as a dict
    - Any non-2xx status OR network error → return None (do NOT raise)

    This call is OPTIONAL — the activity is saved regardless of the result.
    Graceful degradation is the goal: the response will include "game": null
    when game-service is unreachable.
    """
    url = f"{settings.game_service_url}/v1/games/{game_id}"
    try:
        headers = await get_auth_headers()
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
    except (httpx.RequestError, httpx.HTTPStatusError):
        return None


# ---------------------------------------------------------------------------
# Endpoints — pre-written, they call your two functions above
# ---------------------------------------------------------------------------

@app.get("/health")
def health():
    return {"status": "ok", "service": "activity-service"}


@app.post("/v1/activities", response_model=schemas.ActivityOut, status_code=201)
async def create_activity(data: schemas.ActivityCreate, db: Session = Depends(get_db)):
    await validate_user(data.user_id)
    activity = repository.create_activity(db, data)
    game_data = await fetch_game(activity.game_id)
    result = schemas.ActivityOut.model_validate(activity)
    result.game = game_data
    publish_message(
        exchange="gamehub.events",
        routing_key="activity.logged",
        payload=result.model_dump()
    )
    return result


@app.get("/v1/activities", response_model=schemas.ActivityList)
async def list_activities(limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    activities, total = repository.list_activities(db, limit=limit, offset=offset)
    items = []
    for a in activities:
        game_data = await fetch_game(a.game_id)
        items.append({
            "id": a.id,
            "user_id": a.user_id,
            "action": a.action,
            "duration_minutes": a.duration_minutes,
            "created_at": a.created_at,
            "game": game_data,
        })
    return schemas.ActivityList(items=items, total=total, limit=limit, offset=offset)


@app.get("/v1/activities/user/{user_id}", response_model=schemas.ActivityList)
async def list_user_activities(
    user_id: str, limit: int = 20, offset: int = 0, db: Session = Depends(get_db)
):
    activities, total = repository.list_user_activities(db, user_id, limit=limit, offset=offset)
    items = []
    for a in activities:
        game_data = await fetch_game(a.game_id)
        items.append({
            "id": a.id,
            "user_id": a.user_id,
            "action": a.action,
            "duration_minutes": a.duration_minutes,
            "created_at": a.created_at,
            "game": game_data,
        })
    return schemas.ActivityList(items=items, total=total, limit=limit, offset=offset)
