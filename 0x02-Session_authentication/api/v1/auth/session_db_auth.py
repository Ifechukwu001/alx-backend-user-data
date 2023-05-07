#!/usr/bin/env python3
"""Module for SessionBDAuth
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from os import getenv


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth Class"""

    def create_session(self, user_id=None):
        """Creates a new UserSession object
        Returns:
            str: Session ID
        """
        session_id = super().create_session(user_id)
        if session_id is not None:
            session = UserSession(user_id=user_id,
                                  session_id=session_id,
                                  )
            session.save()
            self.user_id_by_session_id[session_id
                                       ]["created_at"
                                         ] = session.created_at
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """Gets user_id based on session_id from database
        Returns:
            str: User ID
        """
        UserSession.load_from_file()
        sessions = UserSession.search({"session_id": session_id})
        for session in sessions:
            sess_dict = {"user_id": session.user_id,
                         "created_at": session.created_at}
            self.user_id_by_session_id[session.session_id] = sess_dict
        return super().user_id_for_session_id(session_id)

    def destroy_session(self, request=None):
        """Destroys a session"""
        session_id = request.cookies.get(getenv("SESSION_NAME"))
        UserSession.load_from_file()
        sessions = UserSession.search({"session_id": session_id})
        for session in sessions:
            session.remove()
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
