from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, JSON, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Association table for many-to-many relationship between words and groups
word_groups = Table(
    'word_groups',
    Base.metadata,
    Column('word_id', Integer, ForeignKey('words.id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('groups.id'), primary_key=True)
)

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    kanji = Column(String, nullable=False)
    romaji = Column(String, nullable=False)
    english = Column(String, nullable=False)
    parts = Column(JSON, nullable=False)

    # Relationships
    groups = relationship("Group", secondary=word_groups, back_populates="words")
    review_items = relationship("WordReviewItem", back_populates="word")

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    words_count = Column(Integer, default=0)

    # Relationships
    words = relationship("Word", secondary=word_groups, back_populates="groups")
    study_sessions = relationship("StudySession", back_populates="group")

class StudyActivity(Base):
    __tablename__ = "study_activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)

    # Relationships
    study_sessions = relationship("StudySession", back_populates="study_activity")

class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    study_activity_id = Column(Integer, ForeignKey("study_activities.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    group = relationship("Group", back_populates="study_sessions")
    study_activity = relationship("StudyActivity", back_populates="study_sessions")
    word_review_items = relationship("WordReviewItem", back_populates="study_session")

class WordReviewItem(Base):
    __tablename__ = "word_review_items"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    study_session_id = Column(Integer, ForeignKey("study_sessions.id"), nullable=False)
    correct = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    word = relationship("Word", back_populates="review_items")
    study_session = relationship("StudySession", back_populates="word_review_items")

    @property
    def correct_count(self):
        """Helper property to count correct reviews for a word"""
        return len([item for item in self.word.review_items if item.correct])

    @property
    def wrong_count(self):
        """Helper property to count incorrect reviews for a word"""
        return len([item for item in self.word.review_items if not item.correct]) 