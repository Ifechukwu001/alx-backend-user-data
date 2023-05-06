#!/usr/bin/env python3
"""Module for Session Auth Expiration
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class
    """

    def __init__(self):
        """Initialize the class"""
        super().__init__()
        duration =  getenv("SESSION_DURATION")
        if duration:
            self.session_duration = int(duration)
        else:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Creates a new session
        Returns:
            str: Session ID
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {"user_id": user_id,
                                                  "created_at": datetime.now(),
                                                  }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Gets the user_id for a session_id
        Returns:
            str: User ID
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session["user_id"]
        if "created_at" not in session:
            return None
        time_difference = datetime.now() - session["created_at"]
        if time_difference.seconds >= self.session_duration:
            return None
        return session["user_id"]
