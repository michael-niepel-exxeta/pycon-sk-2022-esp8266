from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime

from . import models, schemas


def get_scores_by_id(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Score).order_by(models.Score.id.desc()).offset(skip).limit(limit).all()

def get_scores_by_time(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Score).order_by(models.Score.time).offset(skip).limit(limit).all()

def get_score(db: Session, score_id: int):
    return db.query(models.Score).filter(models.Score.id == score_id).first()


def create_score(db: Session, score: schemas.ScoreCreate):
    created = datetime.now()
    db_score = models.Score(time=score.time, created=created)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score

def update_score(db:Session, score_id: int, score: schemas.ScoreUpdate):
    db_score = get_score(db, score_id=score_id)
    db_score.name = score.name
    db.commit()
    db.refresh(db_score)
    return db_score
    
