import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, StudyActivity  # Import necessary models and repositories
from repositories import StudyActivityRepository

# Set up a test database in memory
DATABASE_URL = "sqlite:///:memory:"  # In-memory SQLite database
engine = create_engine(DATABASE_URL, echo=True)

# Create all tables in the test database before running the tests
Base.metadata.create_all(bind=engine)

# Create a sessionmaker bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")  # Create session once for the whole module
def db_session():
    """Fixture to provide a new database session for each test."""
    session = SessionLocal()
    yield session
    session.close()

@pytest.fixture
def study_activity_repo(db_session):
    """Fixture to provide an instance of StudyActivityRepository."""
    return StudyActivityRepository(db_session)

@pytest.fixture
def test_study_activity(db_session):
    """Fixture to add a sample study activity to the database."""
    study_activity = StudyActivity(name="Reading Practice", url="https://example.com/reading")
    db_session.add(study_activity)
    db_session.commit()
    db_session.refresh(study_activity)
    return study_activity

def test_create_study_activity(study_activity_repo):
    """Test creating a new study activity."""
    study_activity = study_activity_repo.create(name="Writing Practice", url="https://example.com/writing")
    assert study_activity is not None
    assert study_activity.name == "Writing Practice"
    assert study_activity.url == "https://example.com/writing"

def test_get_study_activity_by_id(study_activity_repo, test_study_activity):
    """Test getting a study activity by ID."""
    study_activity = study_activity_repo.get_by_id(test_study_activity.id)
    assert study_activity is not None
    assert study_activity.id == test_study_activity.id
    assert study_activity.name == test_study_activity.name
    assert study_activity.url == test_study_activity.url

def test_get_all_study_activities(study_activity_repo):
    """Test getting all study activities."""
    activity1 = study_activity_repo.create(name="Listening Practice", url="https://example.com/listening")
    activity2 = study_activity_repo.create(name="Speaking Practice", url="https://example.com/speaking")
    activities = study_activity_repo.get_all()
    assert len(activities) >= 2
    assert activities[0].name in [activitie.name for activitie in activities]
    assert activities[1].name in [activitie.name for activitie in activities]

def test_update_study_activity(study_activity_repo, test_study_activity):
    """Test updating an existing study activity."""
    updated_activity = study_activity_repo.update(test_study_activity.id, name="Updated Reading Practice", url="https://example.com/updated-reading")
    assert updated_activity is not None
    assert updated_activity.name == "Updated Reading Practice"
    assert updated_activity.url == "https://example.com/updated-reading"

def test_delete_study_activity(study_activity_repo, test_study_activity):
    """Test deleting a study activity."""
    success = study_activity_repo.delete(test_study_activity.id)
    assert success is True
    deleted_activity = study_activity_repo.get_by_id(test_study_activity.id)
    assert deleted_activity is None

def test_get_study_activity_by_name(study_activity_repo, test_study_activity):
    """Test getting a study activity by name."""
    activity = study_activity_repo.get_by_name(test_study_activity.name)
    assert activity is not None
    assert activity.name == test_study_activity.name

