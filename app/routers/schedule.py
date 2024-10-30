from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers import get_schedule, change_schedule_for_presentation, check_presentation_belongs, check_time_is_free
from app.schemas import ScheduleByRooms, ScheduleCreate, ScheduleRow
from typing import List
from app.routers.users import get_current_user_id

router = APIRouter(prefix='/schedule', tags=['Schedule'])

@router.get("/get_all")
def get_schedule_by_rooms(db: Session = Depends(get_db)):
    return get_schedule(db=db)
    
@router.post("/change_shedule_for_presentation", response_model=ScheduleRow)
def change_schedule(schedule: ScheduleCreate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    if check_presentation_belongs(db=db, presentation_id=schedule.presentation_id, user_id=user_id):
        if check_time_is_free(db=db, schedule=schedule):
            return change_schedule_for_presentation(db=db, schedule=schedule)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f'Аудитория в это время занята')
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f'Презентация отсутствует или вам не принадлежит')
        