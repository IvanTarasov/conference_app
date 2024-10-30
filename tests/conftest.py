
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, DATABASE_URL
from app.main import app

client = TestClient(app)

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as client:
        yield client