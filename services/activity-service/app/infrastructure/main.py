import httpx
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from app.database import get_db
from app.config import settings
from app import repository, schemas

app = FastAPI(title="Activity Service API", version="1.0.0")

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2), retry=retry_if_exception_type(httpx.RequestError), reraise=True)
def validate_user(user_id: str) -> None:
    url = f"{settings.user_service_url}/v1/users/{user_id}"
    try:
        response = httpx.get(url, timeout=3.0) 
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        response.raise_for_status() 
    except httpx.HTTPStatusError as e:
        if e.response.status_code >= 500:
            raise httpx.RequestError("User service returned a server error") from e
        raise

def fetch_game(game_id: str) -> dict | None:
    url = f"{settings.game_service_url}/v1/games/{game_id}"
    try:
        response = httpx.get(url, timeout=2.0)
        if response.status_code == 200:
            return response.json()
        return None
    except (httpx.RequestError, httpx.HTTPStatusError):
        return None

@app.post("/v1/activities", response_model=schemas.ActivityOut, status_code=201)
def create_activity(data: schemas.ActivityCreate, db: Session = Depends(get_db)):
    validate_user(data.user_id)
    activity = repository.create_activity(db, data)
    game_data = fetch_game(data.game_id)
    result = schemas.ActivityOut.model_validate(activity)
    result.game = game_data
    return result

@app.get("/v1/activities", response_model=schemas.ActivityList)
def list_activities(limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    activities, total = repository.list_activities(db, limit, offset)
    return schemas.ActivityList(items=[schemas.ActivityOut.model_validate(a) for a in activities], total=total, limit=limit, offset=offset)