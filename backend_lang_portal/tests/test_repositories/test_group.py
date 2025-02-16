import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Group, Word  # Import necessary models and repositories
from repositories import GroupRepository

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
def group_repo(db_session):
    """Fixture to provide an instance of GroupRepository."""
    return GroupRepository(db_session)

@pytest.fixture
def test_group(db_session):
    """Fixture to add a sample group to the database."""
    group = Group(name="Group A")
    db_session.add(group)
    db_session.commit()
    db_session.refresh(group)
    return group

@pytest.fixture
def test_word(db_session):
    """Fixture to add a sample word to the database."""
    word = Word(kanji="日本", romaji="Nihon", english="Japan", parts={"part_of_speech": "noun"})
    db_session.add(word)
    db_session.commit()
    db_session.refresh(word)
    return word

def test_create_group(group_repo):
    """Test creating a new group."""
    group = group_repo.create(name="Group B")
    assert group is not None
    assert group.name == "Group B"

def test_get_group_by_id(group_repo, test_group):
    """Test getting a group by ID."""
    group = group_repo.get_by_id(test_group.id)
    assert group is not None
    assert group.id == test_group.id
    assert group.name == test_group.name

def test_get_all_groups(group_repo):
    """Test getting all groups."""
    group1 = group_repo.create(name="Group B")
    group2 = group_repo.create(name="Group C")
    groups = group_repo.get_all()
    assert len(groups) >= 2
    assert groups[0].name in [group.name for group in groups]
    assert groups[1].name in [group.name for group in groups]

def test_update_group(group_repo, test_group):
    """Test updating an existing group."""
    updated_group = group_repo.update(test_group.id, name="Updated Group A")
    assert updated_group is not None
    assert updated_group.name == "Updated Group A"

def test_delete_group(group_repo, test_group):
    """Test deleting a group."""
    success = group_repo.delete(test_group.id)
    assert success is True
    deleted_group = group_repo.get_by_id(test_group.id)
    assert deleted_group is None

def test_add_word_to_group(group_repo, test_group, test_word):
    """Test adding a word to a group."""
    updated_group = group_repo.add_word(test_group.id, test_word)
    assert updated_group is not None
    assert test_word in updated_group.words
    assert updated_group.words_count == 1

def test_remove_word_from_group(group_repo, test_group, test_word):
    """Test removing a word from a group."""
    group_repo.add_word(test_group.id, test_word)  # Add word first
    updated_group = group_repo.remove_word(test_group.id, test_word)
    assert updated_group is not None
    assert test_word not in updated_group.words
    assert updated_group.words_count == 0

def test_get_group_paginated(group_repo, test_group):
    """Test getting paginated groups."""
    group1 = group_repo.create(name="Group B")
    group2 = group_repo.create(name="Group C")
    
    groups, total = group_repo.get_paginated(page=1, per_page=1)
    assert len(groups) == 1
    assert total == 10  # Including the initial "Group A" from the fixture
    assert groups[0].name in [group.name for group in groups]

