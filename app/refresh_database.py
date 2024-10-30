from app.database import LocalSession, Base, engine
from app.models import *
from uuid import uuid3

def refresh_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = LocalSession()
    try:
        presenter = User(login="presenter", password="12345", role="Presenter")
        presenter_2 = User(login="presenter_2", password="12345", role="Presenter")
        listeners = [User(login="listener_1", password="54321", role="Listener"), User(login="listener_2", password="54321", role="Listener")]

        session.add_all([presenter, presenter_2])
        session.commit()

        session.refresh(presenter)
        session.refresh(presenter_2)
        session.add_all(listeners)
        session.commit()

        presentation = Presentation(title="New presentation 1")
        session.add(presentation)
        presentation.users.append(presenter)
        session.commit()

        presentation2 = Presentation(title="New presentation 2")
        session.add(presentation2)
        presentation2.users.append(presenter_2)
        session.commit()

        presentation3 = Presentation(title="New presentation 3")
        session.add(presentation3)
        presentation3.users.append(presenter)
        presentation3.users.append(presenter_2)
        session.commit()

        rooms = [Room(name="Big room"), Room(name="Small room")]
        session.add_all(rooms)
        session.commit()

        schedules = [Schedule(presentation=presentation, room=rooms[0], date_time="2024-12-31 23:00:00"),
                     Schedule(presentation=presentation2, room=rooms[0], date_time="2024-12-31 22:00:00"),
                     Schedule(presentation=presentation3, room=rooms[1], date_time="2024-12-31 21:00:00")]

        session.add_all(schedules)
        session.commit()

        print("INFO:     Database filled successfully!")
    except Exception as e:
        session.rollback()
        print(f"INFO:     Error occurred: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    refresh_database()
        