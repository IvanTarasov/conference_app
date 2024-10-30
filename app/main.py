from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import schedule, users, presentations
from app.refresh_database import refresh_database
from app.settings import settings

Base.metadata.create_all(bind=engine)

if settings.insert_data_mode:
    refresh_database()

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Веб-приложение 'Конференция'"}

app.include_router(users.router)
app.include_router(schedule.router)
app.include_router(presentations.router)