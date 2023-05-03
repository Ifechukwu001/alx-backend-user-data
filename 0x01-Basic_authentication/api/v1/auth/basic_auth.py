#!/usr/bin/env python3
"""Basic Authentication Module
"""
from api.v1.auth.auth import Auth
import base64
import binascii
from typing import Tuple


class BasicAuth(Auth):
    """BasicAuth Class
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Decodes a base64 header value
        Returns:
            str: The decoded string
        """
        if not base64_authorization_header:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            decoded_msg = base64.b64decode(base64_authorization_header)
        except binascii.Error:
            return None
        return decoded_msg.decode("utf-8")

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> Tuple[str, str]:
        """Extracts user credentials from a decoded base64 string
        Returns:
            tuple(str, str): User email, password
        """
        if not decoded_base64_authorization_header:
            return None, None
        if type(decoded_base64_authorization_header) != str:
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        usermail, password = decoded_base64_authorization_header.split(":")
        return usermail, password
