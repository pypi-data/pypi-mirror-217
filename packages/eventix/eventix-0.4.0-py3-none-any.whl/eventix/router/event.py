import logging

from fastapi import APIRouter

from eventix.pydantic.event import EventModel

log = logging.getLogger(__name__)

router = APIRouter(tags=["event"])


@router.get("/events")
async def events_get():
    return {}


@router.post("/event")
async def events_post(event: EventModel) -> EventModel:
    return event


@router.get("/event/{uid}")
async def events_get(uid: str) -> EventModel:
    return EventModel()


@router.delete("/event/{uid}")
async def events_delete(uid: str) -> None:
    return None
