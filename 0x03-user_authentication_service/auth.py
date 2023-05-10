#!/usr/bin/env python3
"""Module containing the authentication
"""
from sqlalchemy.orm.exc import NoResultFound
from bcrypt import hashpw, gensalt, checkpw
from uuid import uuid4
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user
        Returns:
            User: User object
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
        else:
            raise ValueError(f"User {user.email} already exists.")
        return user
    
    def valid_login(self, email: str, password: str) -> bool:
        """Validates a user
        Returns:
            bool: True if user password matches
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        else:
            return checkpw(password.encode("utf-8"), user.hashed_password)
        
    def create_session(self, email: str) -> str:
        """Creates a session
        Returns:
            str: Session ID
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            pass
        else:
            user.session_id = _generate_uuid()
            self._db._session.add(user)
            self._db._session.commit()
            return user.session_id
        
    def get_user_from_session_id(self, session_id: str) -> User:
        """Gets a User from its session_id
        Returns:
            User: User object
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        else:
            return user
        
    def destroy_session(self, user_id: int):
        """Destroys a user session"""
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            pass
        else:
            user.session_id = None
            self._db._session.add(user)
            self._db._session.commit()


def _hash_password(password: str) -> bytes:
    """Hashes a string password
    Returns:
        bytes: Hashed password
    """
    return hashpw(password.encode("utf-8"), gensalt())


def _generate_uuid() -> str:
    """Generates a UUID string
    Returns:
        str: UUID string
    """
    return str(uuid4())
