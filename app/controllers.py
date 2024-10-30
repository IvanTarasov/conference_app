from sqlalchemy.orm import Session
from . import models, schemas
from typing import List
from datetime import datetime

def get_schedule(db: Session):
    result = db.query(models.Schedule)
    grouped_schedule = {}
    for row in result:
        room = row.room.name
        presentation = {"title": get_presentation_by_id(db=db, id=row.presentation_id).title, "time": row.date_time}

        if room not in grouped_schedule:
            grouped_schedule[room] = {"room": room, "presentations": []}
        
        grouped_schedule[room]["presentations"].append(presentation)

    return list(grouped_schedule.values())

def get_schedule_row_by_presentation(db: Session, presentation: models.Presentation):
    return db.query(models.Schedule).filter(models.Schedule.presentation == presentation).first()

def user_registration(db: Session, user: schemas.UserRegistration):
    db_user = models.User(login=user.login, password=user.password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_login(db: Session, login: str) -> models.User | None:
    return db.query(models.User).filter(models.User.login == login).first()

def get_user_by_id(db: Session, id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == id).first()

def get_user_by_payload(db: Session, user_data: schemas.UserLogin) -> models.User | None:
    return db.query(models.User).filter(models.User.login == user_data.login and models.User.password == user_data.password).first()

def check_user_role(db: Session, user_id: int, role: str) -> bool:
    user = get_user_by_id(db=db, id=user_id)
    if user.role == role:
        return True
    else:
        return False

def check_presentation_belongs(db: Session, presentation_id: int, user_id: int):
    presentation = get_presentation_by_id(db=db, id=presentation_id)
    if presentation is not None:
        user_presentations = db.query(models.Presentation).join(models.Presentation.users).filter(models.User.id == user_id).all()
        if presentation in user_presentations:
            return True
    return False

def remove_presentation_by_id(db: Session, presentation_id: int):
    presentation = db.query(models.Presentation).filter(models.Presentation.id == presentation_id).first()
    db.delete(presentation)
    db.commit()
    return 1

def get_presentations_by_user_id(db: Session, user_id: int):
    user_presentations = db.query(models.Presentation).join(models.Presentation.users).filter(models.User.id == user_id).all()
    result: List[schemas.PresentationWithSchedule] = []
    for p in user_presentations:
        schedule_row = get_schedule_row_by_presentation(db=db, presentation=p)
        data = schemas.PresentationWithSchedule(id=p.id, title=p.title)
        if schedule_row is not None:
            data.room = schedule_row.room.name
            data.date_time = str(schedule_row.date_time)
        result.append(data)
    return result

def get_presentation_by_title(db: Session, title: str) -> models.Presentation | None:
    return db.query(models.Presentation).filter(models.Presentation.title == title).first()

def get_presentation_by_id(db: Session, id: int) -> models.Presentation | None:
    return db.query(models.Presentation).filter(models.Presentation.id == id).first()

def create_presentation(db: Session, presentation: schemas.PresentationCreate, user_id: int):
    user = get_user_by_id(db=db, id=user_id)
    db_presentation = models.Presentation(title = presentation.title)
    db.add(db_presentation)
    db_presentation.users.append(user)
    db.commit()
    db.refresh(db_presentation)
    return db_presentation

def change_schedule_for_presentation(db: Session, schedule: schemas.ScheduleCreate):
    room = db.query(models.Room).filter(models.Room.id == schedule.room_id).first()
    if room is None:
        room = models.Room(id=schedule.room_id, name="Unnamed")
        db.add(room)
        db.commit()
        db.refresh(room)
    presentation = db.query(models.Presentation).filter(models.Presentation.id == schedule.presentation_id).first()
    schedule_row = models.Schedule(presentation=presentation, room=room, date_time=schedule.date_time)
    db.add(schedule_row)
    db.commit()
    db.refresh(schedule_row)
    return schemas.ScheduleRow(presentation_id=presentation.id, date_time=str(schedule_row.date_time), room=schedule_row.room.name, presentation=schedule_row.presentation.title)
    
def check_time_is_free(db: Session, schedule: schemas.ScheduleCreate):
    print(schedule.room_id)
    print(datetime.strptime(schedule.date_time, '%Y-%m-%d %H:%M:%S'))
    time_slot = db.query(models.Schedule).filter(models.Schedule.room_id == schedule.room_id and models.Schedule.date_time == datetime.strptime(schedule.date_time, '%Y-%m-%d %H:%M:%S')).first()
    if time_slot is None:
        return True
    else:
        return False
