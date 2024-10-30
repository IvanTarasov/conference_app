from fastapi import APIRouter, HTTPException, status, Response, Request, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserRegistration, UserLogin
from app.controllers import get_user_by_login, user_registration, get_user_by_payload, get_user_by_id

router = APIRouter(prefix='/auth', tags=['Auth'])

def get_current_user_id(request: Request):
    user_id = request.cookies.get('user_id')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Пользователь не найден')
    return int(user_id)

@router.post("/registration")
def registration(response: Response, user_data: UserRegistration, db: Session = Depends(get_db)):
    user = get_user_by_login(db=db, login=user_data.login)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Пользователь под таким именем уже существует')
        
    if user_data.role != "Listener":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Невозможно зарегистировать пользователя с данной ролью')
    user = user_registration(db=db, user=user_data)
    response.set_cookie(key="user_id", value=user.id, httponly=True)
    return {'user_id': user.id}
    
@router.post("/login")
def auth(response: Response, user_data: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_payload(db=db, user_data=user_data)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Неверный логин или пароль')
        
    response.set_cookie(key="user_id", value=user.id, httponly=True)
    return {'user_id': user.id}

@router.put("/change_role")
def change_role(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user = get_user_by_id(db=db, id=user_id)
    user.role = "Presenter"
    db.commit()
    db.refresh(user)
    return {"message": f"Ваша роль: {user.role}"}
    

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="user_id")
    return {'message': 'Пользователь успешно вышел из системы'}