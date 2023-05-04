#!/usr/bin/env python3
"""Authentication Module for API
"""
from flask import request
from typing import List, TypeVar
import re
import os


class Auth:
    """Auth base class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require_auth method
        Returns:
            bool: False
        """
        if not path:
            return True
        if type(path) == str and not path.endswith("/"):
            path += "/"
        if not excluded_paths:
            return True
        if len(list(filter(lambda x: "*" in x, excluded_paths))):
            patterns = [re.compile(ex_path[:-2]+"."+ex_path[-2:])
                        for ex_path in excluded_paths]
            r_search = [pattern.match(path).string for pattern in patterns
                        if pattern.match(path)]
            if not len(r_search):
                return True
            else:
                return False
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """authorization_header method
        Returns:
            str: None
        """
        if not request:
            return None
        auth_header = request.headers.get("Authorization")
        if auth_header:
            return auth_header
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current_user method
        Returns:
            User: None
        """
        return None

    def session_cookie(self, request=None):
        """Get a session cookie
        Returns:
            Any: Cookie value
        """
        if request is None:
            return None
        cookie_name = os.getenv("SESSION_NAME")
        return request.cookies.get(cookie_name)
