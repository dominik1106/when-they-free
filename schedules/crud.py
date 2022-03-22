import sched
from typing import List
from fastapi.encoders import jsonable_encoder

from .database import collection
from .schemas import Schedule, Participant, TimeFrame, combinedTimes

def get_schedule(schedule_id: str):
    #This returns a regular python dict
    result = collection.find_one({'_id': schedule_id})
    if result is not None:
        #This maps the dict to the Schedule class
        return Schedule(**result)

    raise 'Error, schedule not found!'

def create_schedule(owner: str):
    schedule = Schedule(owner_id=owner)
    owner_participant = Participant(participant_id=owner, busy_times=[])
    schedule.participants.append(owner_participant) #Automatically add Owner as a participant
    schedule_json = jsonable_encoder(schedule)

    collection.insert_one(schedule_json)
    return schedule

def update_schedule(schedule_id: str, busy_times: List[TimeFrame], participant: str):
    result = collection.find_one({'_id': schedule_id})
    if result is not None:
        #Check if participant is updating his own schedule
        schedule = Schedule(**result)
        for p in schedule.participants:
            if p.participant_id == participant:
                p.busy_times = busy_times

        #TODO what if current user isn't part of schedule

        schedule = combinedTimes(schedule=schedule)
        temp = schedule

        schedule = jsonable_encoder(schedule)
        collection.update_one({'_id': schedule_id}, {'$set': schedule})
        return temp
    
    else: #TODO Error handling
        raise 404