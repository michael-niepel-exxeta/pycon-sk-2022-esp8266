from sqlalchemy import Column, Integer, Float, String, DateTime

from .database import Base


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    time = Column(Float)
    created = Column(DateTime)