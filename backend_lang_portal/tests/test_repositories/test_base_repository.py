import pytest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from repositories import BaseRepository  # Assuming your class is in base_repository.py

Base = declarative_base()

class DataModel(Base):
    __tablename__ = "test_model"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    def __init__(self, name: str):
        self.name = name


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    session = TestingSessionLocal()
    yield session
    session.close()

def test_create(db_session: Session):
    repo = BaseRepository[DataModel](db_session, DataModel)
    instance = repo.create(name="Test Name")
    assert instance.id is not None
    assert instance.name == "Test Name"

def test_get_by_id(db_session: Session):
    repo = BaseRepository[DataModel](db_session, DataModel)
    instance = repo.create(name="Test Item")
    fetched_instance = repo.get_by_id(instance.id)
    assert fetched_instance is not None
    assert fetched_instance.id == instance.id
    assert fetched_instance.name == "Test Item"

def test_get_all(db_session: Session):
    repo = BaseRepository[DataModel](db_session, DataModel)
    repo.create(name="Item 1")
    repo.create(name="Item 2")
    items = repo.get_all()
    assert len(items) == 2

def test_update(db_session: Session):
    repo = BaseRepository[DataModel](db_session, DataModel)
    instance = repo.create(name="Old Name")
    updated_instance = repo.update(instance.id, name="New Name")
    assert updated_instance is not None
    assert updated_instance.name == "New Name"

def test_delete(db_session: Session):
    repo = BaseRepository[DataModel](db_session, DataModel)
    instance = repo.create(name="To Be Deleted")
    assert repo.delete(instance.id) is True
    assert repo.get_by_id(instance.id) is None

def test_delete_non_existent(db_session: Session):
    repo = BaseRepository[DataModel](db_session, DataModel)
    assert repo.delete(999) is False
