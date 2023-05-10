#!/usr/bin/env python3
"""Module containing the authentication
"""
from sqlalchemy.orm.exc import NoResultFound
from bcrypt import hashpw, gensalt
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


def _hash_password(password: str) -> bytes:
    """Hashes a string password
    Returns:
        bytes: Hashed password
    """
    return hashpw(password.encode("utf-8"), gensalt())
