from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_session
from app.db.models import Event
from sqlalchemy import select
from app.schemas.schemas import EventBase, ShowEvent, UpdateEvent
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.get("/", response_model=list[EventBase], status_code=200)
async def get_events(db: AsyncSession = Depends(get_async_session)):
    query = select(Event)
    query_result = await db.scalars(query)
    result = query_result.all()
    return result

@router.post("/", response_model=ShowEvent, status_code=201)
async def create_event(event:EventBase, db: AsyncSession = Depends(get_async_session)):
    new_event = Event(**event.model_dump())
    db.add(new_event)
    await db.commit()
    return new_event

@router.patch("/{event_id}", response_model=ShowEvent, status_code=202)
async def update_event(event_id: int, event: UpdateEvent, db : AsyncSession = Depends(get_async_session)):
    query = select(Event).where(Event.id == event_id)
    query_result = await db.scalars(query)
    result = query_result.first()

    if not result:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    for key, value in event.model_dump().items():
        if value is not None:
            setattr(result, key, value)
    
    await db.commit()

    
    return result

@router.delete("/{event_id}", status_code=204)
async def delete_delete(event_id: int, db: AsyncSession = Depends((get_async_session))):
    query = select(Event).where(Event.id == event_id)
    result_query = await db.scalars(query)
    result = result_query.first()

    if not result:
        raise HTTPException(status_code=404, detail="Evento no encontrado o ya fue borrado")
    
    await db.delete(result)
    await db.commit()
    return None

