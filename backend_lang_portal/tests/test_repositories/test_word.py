import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Word, Group  # Import necessary models and repositories
from repositories import WordRepository

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
def word_repo(db_session):
    """Fixture to provide an instance of WordRepository."""
    return WordRepository(db_session)

@pytest.fixture
def test_word(db_session):
    """Fixture to add a sample word to the database."""
    word = Word(kanji="日本", romaji="Nihon", english="Japan", parts={"part_of_speech": "noun"})
    db_session.add(word)
    db_session.commit()
    db_session.refresh(word)
    return word

@pytest.fixture
def test_group(db_session):
    """Fixture to add a sample group to the database."""
    group = Group(name="Group A")
    db_session.add(group)
    db_session.commit()
    db_session.refresh(group)
    return group

def test_create_word(word_repo):
    """Test creating a new word."""
    word = word_repo.create(kanji="東京", romaji="Tokyo", english="Tokyo", parts={"part_of_speech": "noun"})
    assert word is not None
    assert word.kanji == "東京"
    assert word.romaji == "Tokyo"
    assert word.english == "Tokyo"

def test_get_word_by_kanji(word_repo, test_word):
    """Test getting a word by kanji."""
    word = word_repo.get_by_kanji("日本")
    assert word is not None
    assert word.kanji == "日本"
    assert word.romaji == "Nihon"
    assert word.english == "Japan"

def test_get_word_by_group(word_repo, test_word, test_group):
    """Test getting words by group."""
    test_group.words.append(test_word)
    word_repo.db.commit()
    
    words_in_group = word_repo.get_by_group(test_group.id)
    assert len(words_in_group) == 1
    assert words_in_group[0].kanji == "日本"

def test_update_word(word_repo, test_word):
    """Test updating an existing word."""
    updated_word = word_repo.update(test_word.id, kanji="新しい日本")
    assert updated_word is not None
    assert updated_word.kanji == "新しい日本"

def test_delete_word(word_repo, test_word):
    """Test deleting a word."""
    success = word_repo.delete(test_word.id)
    assert success is True
    deleted_word = word_repo.get_by_id(test_word.id)
    assert deleted_word is None

def test_get_word_paginated(word_repo, test_group):
    """Test getting paginated words."""
    word1 = word_repo.create(kanji="さくら", romaji="sakura", english="cherry blossom", parts={"part_of_speech": "noun"})
    word2 = word_repo.create(kanji="富士山", romaji="Fujisan", english="Mount Fuji", parts={"part_of_speech": "noun"})
    
    # Add words to group
    test_group.words.extend([word1, word2])
    word_repo.db.commit()

    words, total = word_repo.get_by_group_paginated(group_id=test_group.id, page=1, per_page=1)
    assert len(words) == 1
    assert total == 2
    assert words[0].kanji in ["さくら", "富士山"]

