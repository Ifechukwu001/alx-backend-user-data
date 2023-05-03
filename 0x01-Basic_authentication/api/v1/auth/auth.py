#!/usr/bin/env python3
"""Authentication Module for API
"""
from flask import request
from typing import List, TypeVar


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
