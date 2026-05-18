# Application layer — business logic.
#
# Calls repository functions and returns Pydantic schemas (not raw ORM objects).
# Raises ValueError when a game is not found — routes.py turns it into a 404.
#
# Implement these four functions:
# - add_game(db, data) -> GameOut
# - fetch_game(db, game_id) -> GameOut        (raises ValueError if not found)
# - fetch_all_games(db, limit, offset) -> GameList
# - find_games(db, q, limit, offset) -> GameList   (delegates to search_games in repository)
from sqlalchemy.orm import Session
from app import repository
from app.schemas import *

def add_game(db: Session, data: GameCreate) -> GameOut:
    game = repository.create_game(db, data)
    return GameOut.model_validate(game)

def fetch_game(db: Session, game_id: str) -> GameOut:
    game = repository.get_game(db, game_id)
    if not game:
        raise ValueError(f"Game with ID {game_id} not found")
    return GameOut.model_validate(game)

def fetch_all_games(db: Session, limit: int, offset: int) -> GameList:
    games, total = repository.list_games(db, limit, offset)
    return GameList(
        items=[GameOut.model_validate(g) for g in games],
        total=total,
        limit=limit,
        offset=offset
    )

def find_games(db: Session, q: str, limit: int, offset: int) -> GameList:
    games, total = repository.search_games(db, q, limit, offset)
    return GameList(
        items=[GameOut.model_validate(g) for g in games],
        total=total,
        limit=limit,
        offset=offset
    )