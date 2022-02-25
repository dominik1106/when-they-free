from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId


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
    begin: float = Field(ge=0, le=168,)
    end: float = Field(ge=0, le=168)

class Participant(BaseModel):
    participant_id: str
    busy_times: Optional[List[TimeFrame]]

class Schedule(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    owner_id: str
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