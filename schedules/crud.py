from fastapi.encoders import jsonable_encoder

from .database import collection
from .schemas import Schedule, Participant, combinedTimes

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

def update_schedule(schedule_id: str, participant: Participant):
    result = collection.find_one({'_id': schedule_id})
    if result is not None:
        #Check if participant is updating his own schedule
        schedule = Schedule(**result)
        for p in schedule.participants:
            if p.participant_id == participant.participant_id:
                print('found the right participant!')
                p.busy_times = participant.busy_times

        schedule = combinedTimes(schedule=schedule)

        schedule = jsonable_encoder(schedule)
        print(schedule)
        collection.update_one({'_id': schedule_id}, {'$set': schedule})
        return 'success'
    
    else: #TODO Error handling
        raise 404