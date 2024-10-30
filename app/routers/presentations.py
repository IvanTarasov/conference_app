from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers import check_user_role, create_presentation, get_presentations_by_user_id, get_presentation_by_id, check_presentation_belongs, remove_presentation_by_id, get_presentation_by_title
from app.schemas import PresentationWithSchedule, PresentationCreate, PresentationUpdate
from typing import List
from app.routers.users import get_current_user_id

router = APIRouter(prefix='/presentation', tags=['Presentations'])

@router.get("/get_my", response_model=List[PresentationWithSchedule])
def get_user_presentations(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    if check_user_role(db=db, user_id=user_id, role="Presenter"):
        return get_presentations_by_user_id(db=db, user_id=user_id)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Операции с презентациями вам не доступны')

@router.post("/create", response_model=PresentationWithSchedule)
def new_presentation(presentation: PresentationCreate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    if check_user_role(db=db, user_id=user_id, role="Presenter"):
        db_presentation = get_presentation_by_title(db=db, title=presentation.title)
        if db_presentation is None:
            return create_presentation(db=db, presentation=presentation, user_id=user_id)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Такая презентация уже существует')
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Операции с презентациями вам не доступны')
    
            
@router.put("/update", response_model=PresentationWithSchedule)
def put_presentation(presentation: PresentationUpdate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    if check_user_role(db=db, user_id=user_id, role="Presenter"):
        if check_presentation_belongs(db=db, presentation_id=presentation.id, user_id=user_id):
            db_presentation = get_presentation_by_id(db=db, id=presentation.id)
            db_presentation.title = presentation.title
            db.commit()
            db.refresh(db_presentation)
            return db_presentation
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f'Презентация отсутствует или вам не принадлежит')
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Операции с презентациями вам не доступны')
    
@router.delete("/delete")
def delete_presentation(presentation_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    if check_user_role(db=db, user_id=user_id, role="Presenter"):
        if check_presentation_belongs(db=db, presentation_id=presentation_id, user_id=user_id):
            return {"message": f"Удалено записей: {remove_presentation_by_id(db=db, presentation_id=presentation_id)}"}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f'Презентация отсутствует или вам не принадлежит')
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Операции с презентациями вам не доступны')