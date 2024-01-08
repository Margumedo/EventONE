from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import ReservationBase, ShowReservation, ReservationUpdate
from app.db.database import get_async_session
from app.db.models import Reservation, Event
from sqlalchemy import select
from typing import List, Optional

router = APIRouter(
    prefix="/reservation",
    tags=["Reservations"]
)


@router.get("/", response_model=Optional[List[ShowReservation]], status_code=200)
async def get_reservations(db: AsyncSession = Depends(get_async_session)):
    query = select(Reservation)
    query_result = await db.scalars(query)
    result = query_result.all()
    return result

@router.post("/", response_model=ShowReservation, status_code=201)
async def create_reservation(reservation: ReservationBase, db: AsyncSession = Depends(get_async_session)):
    #Primero verifico que el evento exista y guardo la capacidad del evento
    query = select(Event.capacity).where(Event.id == reservation.event_id)
    query_result = await db.scalars(query)
    result = query_result.first()
    max_capacity = result

    if not result:
        raise HTTPException(status_code=404, detail="Event not found")
    
    #Luego valido en numero de persons que tienen reservado ese evento
    query = select(Reservation.num_guests).where(Event.id == reservation.event_id)
    query_result = await db.scalars(query)
    num_guest_array = query_result.all()
    num_guest_sum = sum(num_guest_array)

    #Luego verifico que la capacidad maxima no se exedida con mi reserva
    if reservation.num_guests + num_guest_sum > max_capacity:
        raise HTTPException(status_code=400, detail="No enough seats available")

    
    new_reservation = Reservation(**reservation.model_dump(exclude_none=True))
    db.add(new_reservation)
    await db.commit()
    return new_reservation

@router.patch("/{reservation_id}", response_model=ShowReservation, status_code=202)
async def update_reservation(reservation_id: int, reservation: ReservationUpdate, db: AsyncSession = Depends(get_async_session)):
    #primero verifico que el evento exista y me traigo la capcidad
    query = select()
    
    query = select(Reservation).where(Reservation.id == reservation_id)
    query_result = await db.scalars(query)
    result = query_result.first()

    if not result:
        raise HTTPException(status_code=404, detail="Reservation no found")
    
    for key, value in reservation.model_dump().items():
        if value is not None:
            setattr(result, key, value)
      
    await db.commit()
    await db.refresh(result)
    return result
    
@router.delete("/{reservation_id}", status_code=204)
async def delete_reservation(reservation_id: int, db: AsyncSession = Depends(get_async_session)):
    query = select(Reservation).where(Reservation.id == reservation_id)
    query_result = await db.scalars(query)
    result = query_result.first()

    if not result: 
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    await db.delete(result)
    await db.commit()
    return None