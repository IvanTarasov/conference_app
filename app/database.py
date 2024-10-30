from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from app.settings import settings

engine = create_engine(
    f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_server}:{settings.postgres_port}/{settings.postgres_db}"
)


LocalSession = sessionmaker(engine)

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
