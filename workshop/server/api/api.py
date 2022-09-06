from typing import Union

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/leaderboard/", response_model=list[schemas.Score])
def read_scores(by_id: bool = False, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if by_id:
        return crud.get_scores_by_id(db, skip, limit)    
    return crud.get_scores_by_time(db, skip, limit)

@app.post("/leaderboard/", response_model=schemas.Score)
def create_score(score: schemas.ScoreCreate, db: Session = Depends(get_db)):
    return crud.create_score(db, score=score)

@app.patch("/leaderboard/{score_id}", response_model=schemas.Score)
def update_score(score_id: int, score: schemas.ScoreUpdate, db: Session = Depends(get_db)):
    return crud.update_score(db, score_id=score_id, score=score)