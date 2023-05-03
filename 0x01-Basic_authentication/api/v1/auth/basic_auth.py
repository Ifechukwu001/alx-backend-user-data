#!/usr/bin/env python3
"""Basic Authentication Module
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """BasicAuth Class
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Extracts the Base64 part of the AUth header
        Returns:
            str: Base64 string
        """
        if not authorization_header:
            return None
        if type(authorization_header) != str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        b64 = authorization_header.split(" ")[1]
        return b64
