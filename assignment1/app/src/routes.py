from fastapi import APIRouter, HTTPException
from typing import List
from .models import Event
from .file_storage import EventFileManager
from .event_analyzer import EventAnalyzer

router = APIRouter()

@router.get("/events", response_model=List[Event])
async def get_all_events():
    events = EventFileManager.read_events_from_file()
    return events


@router.get("/events/filter", response_model=List[Event])
async def get_events_by_filter(date: str = None, organizer: str = None, status: str = None, event_type: str = None):
    events = EventFileManager.read_events_from_file()
    filtered = []
    for event in events:
        if (date is None or event.date == date) and (organizer is None or event.organizer.name == organizer) and (status is None or event.status == status) and (event_type is None or event.type == event_type):
            filtered.append(event)
    return filtered


@router.get("/events/{event_id}", response_model=Event)
async def get_event_by_id(event_id: int):
    events = EventFileManager.read_events_from_file()

    for event in events:
        if event["id"] == event_id:
            return event
#    raise HTTPException(status_code=404, detail="Event could not be found")

@router.post("/events", response_model=Event)
async def create_event(event: Event):
    original_events = EventFileManager.read_events_from_file()
    for existing_event in original_events:
        if existing_event.id == event.id:
            raise HTTPException(status_code=400, detail="Event ID already exists")
    original_events.append(event)

    EventFileManager.write_events_to_file(original_events)
    return event

@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: Event):
        old_events = EventFileManager.read_events_from_file()
        event_index = None
        for i, old_event in enumerate(old_events):
            if old_event.id == event_id:
                event_index = i
                break

        if event_index is None:
            raise HTTPException(status_code=404, detail="Event not found")

        old_events[event_index] = event

        EventFileManager.write_events_to_file(old_events)
        return event


@router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    old_events = EventFileManager.read_events_from_file()
    new_events = list(filter(lambda event: event.id != event_id, old_events))
    if len(old_events) == len(new_events):
        raise HTTPException(status_code=404, detail="Event not found")

    EventFileManager.write_events_to_file(new_events)
    return {"message": "Event deleted successfully"}


@router.get("/events/joiners/multiple-meetings")
async def get_joiners_multiple_meetings():
    events = EventFileManager.read_events_from_file()
    event_analyzer = EventAnalyzer(events)
    joiners_multiple_meetings = event_analyzer.get_joiners_multiple_meetings_method()

    if not joiners_multiple_meetings:
        return {"message": "No joiners attending at least 2 meetings were found"}

    return joiners_multiple_meetings
