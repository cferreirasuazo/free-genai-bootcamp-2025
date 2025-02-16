import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, WordReviewItem, StudySession, Word  # Import necessary models
from repositories import WordReviewItemRepository  # Import the repository from the repositories file

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
def word_review_item_repo(db_session):
    """Fixture to provide an instance of WordReviewItemRepository."""
    return WordReviewItemRepository(db_session)

@pytest.fixture
def test_word(db_session):
    """Fixture to add a sample word to the database."""
    word = Word(kanji="漢字", romaji="kanji", english="kanji", parts=[])
    db_session.add(word)
    db_session.commit()
    db_session.refresh(word)
    return word

@pytest.fixture
def test_study_session(db_session):
    """Fixture to add a sample study session to the database."""
    session = StudySession(group_id=1, study_activity_id=1)
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)
    return session

@pytest.fixture
def test_word_review_item(db_session, test_word, test_study_session):
    """Fixture to add a sample word review item to the database."""
    review_item = WordReviewItem(word_id=test_word.id, study_session_id=test_study_session.id, correct=True)
    db_session.add(review_item)
    db_session.commit()
    db_session.refresh(review_item)
    return review_item

def test_create_word_review_item(word_review_item_repo, test_word, test_study_session):
    """Test creating a new word review item."""
    review_item = word_review_item_repo.create(word_id=test_word.id, study_session_id=test_study_session.id, correct=True)
    assert review_item is not None
    assert review_item.word_id == test_word.id
    assert review_item.study_session_id == test_study_session.id
    assert review_item.correct is True

def test_get_word_review_items_by_word(word_review_item_repo, test_word, test_word_review_item):
    """Test getting word review items by word ID."""
    review_items = word_review_item_repo.get_by_word(test_word.id)
    assert len(review_items) > 0
    assert all(item.word_id == test_word.id for item in review_items)

def test_get_word_review_items_by_session(word_review_item_repo, test_study_session, test_word_review_item):
    """Test getting word review items by session ID."""
    review_items = word_review_item_repo.get_by_session(test_study_session.id)
    assert len(review_items) > 0
    assert all(item.study_session_id == test_study_session.id for item in review_items)

def test_correct_count_property(word_review_item_repo, test_word):
    """Test the correct_count property."""
    review_item1 = word_review_item_repo.create(word_id=test_word.id, study_session_id=1, correct=True)
    review_item2 = word_review_item_repo.create(word_id=test_word.id, study_session_id=1, correct=True)
    review_item3 = word_review_item_repo.create(word_id=test_word.id, study_session_id=1, correct=False)
    
    correct_count = review_item1.correct_count  # Accessing the property directly
    assert correct_count == 2  # Expecting 2 correct reviews for this word

