#!/usr/bin/env python3
"""Module containing the DB class
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Gets a User
        Returns:
            User: a User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user
    
    def find_user_by(self, *args, **kwargs) -> User:
        """Finds user
        Returns:
            User: User object
        """
        session_query = self._session.query(User)
        for attr, value in kwargs.items():
            if attr not in User.__dict__:
                raise InvalidRequestError
            session_query = session_query.filter(getattr(User, attr) == value)
        result = session_query.first()
        if not result:
            raise NoResultFound
        return result
