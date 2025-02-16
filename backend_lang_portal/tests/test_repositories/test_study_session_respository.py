import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, StudySession, StudyActivity, Group  # Import necessary models
from repositories import StudySessionRepository  # Import the repository from the repositories file

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
def study_session_repo(db_session):
    """Fixture to provide an instance of StudySessionRepository."""
    return StudySessionRepository(db_session)

@pytest.fixture
def test_group(db_session):
    """Fixture to add a sample group to the database."""
    group = Group(name="Group 1")
    db_session.add(group)
    db_session.commit()
    db_session.refresh(group)
    return group

@pytest.fixture
def test_study_activity(db_session):
    """Fixture to add a sample study activity to the database."""
    activity = StudyActivity(name="Reading Practice", url="https://example.com/reading")
    db_session.add(activity)
    db_session.commit()
    db_session.refresh(activity)
    return activity

@pytest.fixture
def test_study_session(db_session, test_group, test_study_activity):
    """Fixture to add a sample study session to the database."""
    session = StudySession(group_id=test_group.id, study_activity_id=test_study_activity.id)
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)
    return session

def test_create_study_session(study_session_repo, test_group, test_study_activity):
    """Test creating a new study session."""
    study_session = study_session_repo.create(group_id=test_group.id, study_activity_id=test_study_activity.id)
    assert study_session is not None
    assert study_session.group_id == test_group.id
    assert study_session.study_activity_id == test_study_activity.id

def test_get_study_session_by_id(study_session_repo, test_study_session):
    """Test getting a study session by ID."""
    study_session = study_session_repo.get_by_id(test_study_session.id)
    assert study_session is not None
    assert study_session.id == test_study_session.id

def test_get_study_sessions_by_group(study_session_repo, test_group):
    """Test getting all study sessions for a specific group."""
    session1 = study_session_repo.create(group_id=test_group.id, study_activity_id=1)
    session2 = study_session_repo.create(group_id=test_group.id, study_activity_id=2)
    sessions = study_session_repo.get_by_group(test_group.id)
    assert len(sessions) >= 2
    assert all(session.group_id == test_group.id for session in sessions)

