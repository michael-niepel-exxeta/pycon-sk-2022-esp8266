from typing import Optional
from datetime import datetime
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
    time: float

    class Config:
        orm_mode = True