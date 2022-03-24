from sqlite3 import Time
from typing import Optional, List
from fastapi import HTTPException, status
from pydantic import BaseModel, Field, validator
from bson import ObjectId
import pydantic
from sqlalchemy import false


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class TimeFrame(BaseModel):
    begin: float = Field(ge=0, le=167.5,)
    end: float = Field(ge=0.5, le=168)

    @validator('end')
    def timeframe_must_be_longer_than_30_minutes(cls, v, values, **kwargs):
        if 'begin' in values and (v-values['begin']) < 0.5:
            raise ValueError('timeframe must be atleast than 30 minutes')
        return v



class Participant(BaseModel):
    participant_id: str
    busy_times: Optional[List[TimeFrame]]

class Schedule(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    owner_id: str
    combined_times: Optional[List[TimeFrame]] = []
    participants: List[Participant] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            'example': {
                'id': 'mongodb-id',
                'owner_id': 'ba408a9f1d5b4a1c8db5fc5dc600faef (uuid4 in hex)',
                'participants': {
                    'participant': 'ba408a9f1d5b4a1c8db5fc5dc600faef (uuid4 in hex)',
                    'busy-times': [
                        {
                            'begin': 13,
                            'end': 14.5
                        },
                        {
                            'begin': 27,
                            'end': 28,
                        },
                    ],
                }
            }
        }

class UpdateSchedule(BaseModel):
    participants: Optional[Participant]

def combinedTimes(schedule: Schedule):
    combinedList: List[TimeFrame] = []

    # Combining all participants busytimes into 1 long list
    for p in schedule.participants:
        combinedList = combinedList + p.busy_times

    i = 0
    ordered = False
    
    # Bubblesort-Style, prob terrible O
    while ordered is False:
        ordered = True
        combinedList.sort(key=lambda x: x.begin)
        while True:
            if (combinedList[i].end - combinedList[i].begin) <= 0.5:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="The minimum length for a timeframe are 30min",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            if i == len(combinedList)-1:
                break
            elif combinedList[i].end >= combinedList[i+1].begin:
                ordered = False
                if combinedList[i+1].end > combinedList[i].end:
                    combinedList[i].end = combinedList[i+1].end
                combinedList.pop(i+1)
            else:
                i = i+1

    schedule.combined_times = combinedList
    return schedule
