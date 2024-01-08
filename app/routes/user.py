from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_session
from app.db.models import User
from sqlalchemy import select
from app.schemas.schemas import ShowUser, UserBase, UpdateUser, ShowEvent
from typing import List
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=List[ShowUser])
async def get_users(db: AsyncSession = Depends(get_async_session)):
    query = select(User)
    query_result = await db.scalars(query)
    result = query_result.unique().all()
    return result

@router.post("/", response_model=UserBase, status_code=201)
async def create_user(new_user: UserBase, db: AsyncSession = Depends(get_async_session)):
    user = User(**new_user.model_dump())
    db.add(user)
    try:
        await db.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="El Usuario o Email ya existe")
    await db.refresh(user)
    return user

@router.get("/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.id == user_id)
    query_result = await db.scalars(query)
    result = query_result.first()
    if result is None:
        raise HTTPException(status_code=404, detail="Usuario no existe")
    return result


@router.get("/{user_id}/events", response_model=List[ShowEvent], status_code=200)
async def get_user_events(user_id: int, db: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.id == user_id)
    query_result = await db.scalars(query)
    result = query_result.first()
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    
    events = result.events

    return events

@router.patch("/{user_id}", response_model=ShowUser, status_code=202)
async def update_user(user_id: int, user: UpdateUser, db: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.id == user_id)
    query_result = await db.scalars(query)
    print(query_result)
    result = query_result.first()
    print(result)
    if result is None:
        raise HTTPException(status_code=404, detail="Usuario no existe")
    
    for key, value in user.model_dump().items():
        if value is not None:
            setattr(result, key, value)
            
    try:
        await db.commit()
    except:
        raise HTTPException(status_code=400, detail="El Usuario o Email ya esta en uso")
    return result

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.id == user_id)
    query_result = await db.scalars(query)
    result = query_result.first()

    if result is None:
        raise HTTPException(status_code=404, detail="El Usuario no existe")
    
    await db.delete(result)
    await db.commit()
    return None