from sqlalchemy.orm import Session
from typing import List, Optional, TypeVar, Generic, Type
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Group, StudyActivity, StudySession, Word, WordReviewItem
from sqlalchemy import desc, asc


T = TypeVar('T')


class BaseRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def get_by_id(self, id: int) -> Optional[T]:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self) -> List[T]:
        return self.db.query(self.model).all()

    def create(self, **kwargs) -> T:
        instance = self.model(**kwargs)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def update(self, id: int, **kwargs) -> Optional[T]:
        instance = self.get_by_id(id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            self.db.commit()
            self.db.refresh(instance)
        return instance

    def delete(self, id: int) -> bool:
        instance = self.get_by_id(id)
        if instance:
            self.db.delete(instance)
            self.db.commit()
            return True
        return False


class WordRepository(BaseRepository[Word]):
    def __init__(self, db: Session):
        super().__init__(db, Word)

    def get_by_kanji(self, kanji: str) -> Optional[Word]:
        return self.db.query(self.model).filter(self.model.kanji == kanji).first()

    def get_by_group(self, group_id: int) -> List[Word]:
        return (self.db.query(self.model)
                .join(self.model.groups)
                .filter(Group.id == group_id)
                .all())

    def get_by_group_paginated(
        self,
        group_id: int,
        page: int = 1,
        sort_by: str = 'english',
        order: str = 'asc',
        per_page: int = 10
    ) -> tuple[List[Word], int]:
        """Get paginated and sorted words for a specific group"""
        query = (self.db.query(self.model)
                 .join(self.model.groups)
                 .filter(Group.id == group_id))

        # Apply sorting
        sort_column = getattr(Word, sort_by, Word.english)
        if order == 'desc':
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

        # Get total count before pagination
        total = query.count()

        # Apply pagination
        offset = (page - 1) * per_page
        words = query.offset(offset).limit(per_page).all()

        return words, total


class GroupRepository(BaseRepository[Group]):
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str) -> Optional[Group]:
        """Create a new group"""
        try:
            group = Group(name=name)
            self.db.add(group)
            self.db.commit()
            self.db.refresh(group)
            return group
        except SQLAlchemyError:
            self.db.rollback()
            return None

    def get_by_id(self, group_id: int) -> Optional[Group]:
        """Get a group by its ID"""
        return self.db.query(Group).filter(Group.id == group_id).first()

    def get_all(self) -> List[Group]:
        """Get all groups"""
        return self.db.query(Group).all()

    def update(self, group_id: int, name: str) -> Optional[Group]:
        """Update a group's name"""
        group = self.get_by_id(group_id)
        if group:
            try:
                group.name = name
                self.db.commit()
                self.db.refresh(group)
                return group
            except SQLAlchemyError:
                self.db.rollback()
                return None
        return None

    def delete(self, group_id: int) -> bool:
        """Delete a group"""
        group = self.get_by_id(group_id)
        if group:
            try:
                self.db.delete(group)
                self.db.commit()
                return True
            except SQLAlchemyError:
                self.db.rollback()
                return False
        return False

    def get_by_name(self, name: str) -> Optional[Group]:
        """Get a group by its name"""
        return self.db.query(Group).filter(Group.name == name).first()

    def add_word(self, group_id: int, word) -> Optional[Group]:
        """Add a word to the group"""
        group = self.get_by_id(group_id)
        if group:
            try:
                group.words.append(word)
                group.words_count = len(group.words)
                self.db.commit()
                self.db.refresh(group)
                return group
            except SQLAlchemyError:
                self.db.rollback()
                return None
        return None

    def remove_word(self, group_id: int, word) -> Optional[Group]:
        """Remove a word from the group"""
        group = self.get_by_id(group_id)
        if group and word in group.words:
            try:
                group.words.remove(word)
                group.words_count = len(group.words)
                self.db.commit()
                self.db.refresh(group)
                return group
            except SQLAlchemyError:
                self.db.rollback()
                return None
        return None

    def get_paginated(self, page: int = 1, sort_by: str = 'name', order: str = 'asc',
                      per_page: int = 10) -> tuple[List[Group], int]:
        """Get paginated and sorted groups"""
        query = self.db.query(Group)

        # Apply sorting
        sort_column = getattr(Group, sort_by, Group.name)
        if order == 'desc':
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

        # Get total count before pagination
        total = query.count()

        # Apply pagination
        offset = (page - 1) * per_page
        groups = query.offset(offset).limit(per_page).all()

        return groups, total


class StudyActivityRepository(BaseRepository[StudyActivity]):
    def __init__(self, db: Session):
        super().__init__(db, StudyActivity)

    def get_by_name(self, name: str) -> Optional[StudyActivity]:
        return self.db.query(self.model).filter(self.model.name == name).first()


class StudySessionRepository(BaseRepository[StudySession]):
    def __init__(self, db: Session):
        super().__init__(db, StudySession)

    def get_by_group(self, group_id: int) -> List[StudySession]:
        return (self.db.query(self.model)
                .filter(self.model.group_id == group_id)
                .all())


class WordReviewItemRepository(BaseRepository[WordReviewItem]):
    def __init__(self, db: Session):
        super().__init__(db, WordReviewItem)

    def get_by_word(self, word_id: int) -> List[WordReviewItem]:
        return (self.db.query(self.model)
                .filter(self.model.word_id == word_id)
                .all())

    def get_by_session(self, session_id: int) -> List[WordReviewItem]:
        return (self.db.query(self.model)
                .filter(self.model.study_session_id == session_id)
                .all())
