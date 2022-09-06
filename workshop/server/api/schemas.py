from typing import Optional
from datetime import datetime, time as dt_time
from pydantic import BaseModel

class ScoreBase(BaseModel):
    ...

class ScoreCreate(ScoreBase):
    time: str

class ScoreUpdate(ScoreBase):
    name: str

class Score(ScoreBase):
    id: int
    created: datetime
    name: Optional[str]
    time: dt_time

    class Config:
        orm_mode = True