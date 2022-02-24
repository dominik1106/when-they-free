from typing import Optional, List
from pydantic import BaseModel
import pymongo
from mongodb_schedule import collection

from .mongodb_schedule import collection


class TimeFrame(BaseModel):
    begin: float
    end: float

class Participant(BaseModel):
    participant_id: str
    schedule: List[TimeFrame]

class ScheduleCreate(BaseModel):
    owner_id: str
    participants: List[Participant] = []

class Schedule(ScheduleCreate):
    _id: str


def create_schedule(owner: str, participants: Optional[Participant]):
    schedule = ScheduleCreate(owner_id=owner, participants=participants)
    schedule_id = collection.insert_one(schedule)
    return schedule_id