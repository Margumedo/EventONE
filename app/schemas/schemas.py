from pydantic import BaseModel, Field, PositiveInt, EmailStr
from datetime import datetime
from typing import Optional
from sqlalchemy.dialects.postgresql import JSONB

#schemas para Usuarios
class UserBase(BaseModel):

    username: str = Field(..., min_length=5, max_length=50, examples=["maicolino"])
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=30, examples=["pass1234"])
    is_admin: bool = Field(False)

class ShowUser(UserBase):

    id: PositiveInt
    created_at: datetime

class CreateUser(UserBase):

    created_at: datetime    

class UpdateUser(BaseModel):
    username: Optional[str] = Field(None, min_length=5, max_length=50, examples=["maicolino"])
    email: Optional[EmailStr] = Field(None)
    password: Optional[str] = Field(None, min_length=8, max_length=30, examples=["pass1234"])
    is_admin: Optional[bool] = Field(None)

#Schemas para Eventos
class EventBase(BaseModel):

    name: str = Field(..., min_length=3, max_length=50, examples=["Incidente de Shibuya"])
    date: datetime
    location: str = Field(..., min_length=3, max_length=50, examples=["Shibuya"])
    capacity: PositiveInt = Field(..., examples=[100])
    content: dict
    user_id: PositiveInt = Field(..., examples=[1])

class ShowEvent(EventBase):

    id: PositiveInt


class UpdateEvent(BaseModel):
    name: str = None
    date: datetime = None
    location: str = None
    capacity: PositiveInt = None
    content: dict = None

#Schemas para reservations

class ReservationBase(BaseModel):
    num_guests: int
    event_id: int
    user_id: int

class ShowReservation(BaseModel):
    id: int
    num_guests: int
    event_id: int
    user_id: int
    created_at: datetime

class ReservationUpdate(BaseModel):
    num_guests: Optional[PositiveInt] = Field(None, examples=[1])
    event_id: Optional[PositiveInt] = Field(None, examples=[1])
    user_id: Optional[PositiveInt] = Field(None, examples=[10])
    
#Schemas para los comentarios

class contentSchema(BaseModel):
    title: str = Field(..., examples=["Titulo"])
    text: str = Field(..., examples=["Texto"])
    raiting: int = Field(..., ge=1, le=10, examples=[5])

class CommentBase(BaseModel):

    content: contentSchema
    user_id: PositiveInt = Field(..., examples=[1])
    event_id: PositiveInt = Field(..., examples=[10])

class ShowComment(CommentBase):
    id: PositiveInt
    created_at: datetime

class UpdateComment(BaseModel):
    content: Optional[contentSchema] = Field(None)
    user_id: Optional[PositiveInt] = Field(None, examples=[1])
    event_id:  Optional[PositiveInt] = Field(None, examples=[10])