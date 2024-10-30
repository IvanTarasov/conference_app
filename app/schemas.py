from pydantic import BaseModel, field_validator, Field
from typing import List
from datetime import datetime


class UserRegistration(BaseModel):
    login: str = Field(..., description="Логин пользователя, уникальный")
    password: str = Field(..., description="Пароль пользователя")
    role: str = Field(default="Listener", description="Роль пользователя")

class UserLogin(BaseModel):
    login: str = Field(..., description="Логин пользователя, уникальный")
    password: str = Field(..., description="Пароль пользователя")

class PresentationCreate(BaseModel):
    title: str = Field(..., description="Название презентации, уникальное")

class PresentationWithSchedule(PresentationCreate):
    id: int = Field(default=..., description="ID презентации")
    room: str = Field(default="Не назначена", description="Название аудитории")
    date_time: str = Field(default="Не выбрано", description="Дата и время презентации")

class PresentationUpdate(PresentationCreate):
    id: int = Field(default=..., description="ID презентации")

class PresentationForSchedule(BaseModel):
    title: str = Field(..., description="Название презентации")
    time: datetime = Field(..., description="Дата и время презентации")

class ScheduleBase(BaseModel):
    date_time: str = Field(default=..., description="Дата и время презентации")

    @field_validator("date_time")
    def validate_date_time(cls, value):
        try:
            dt = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            
            if dt.minute != 0 or dt.second != 0:
                raise ValueError('Минуты и секунды не указываются')
        except ValueError:
            raise ValueError('Дата и время презентации должны быть формата YYYY-MM-DD HH:00:00')
        return value

class ScheduleCreate(ScheduleBase):
    presentation_id: int = Field(default=..., description="ID презентации")
    room_id: int = Field(default=-1, description="ID аудитории")

class ScheduleRow(ScheduleBase):
    presentation_id: int = Field(default=..., description="ID презентации")
    room: str = Field(default=..., description="Название аудитории")
    presentation: str = Field(default=..., description="Название презентации")
    
class ScheduleByRooms(BaseModel):
    room: str = Field(default=..., description="Название аудитории")
    presentations: List[PresentationForSchedule] = Field(default=..., description="Список презентаций в данной аудитории")
