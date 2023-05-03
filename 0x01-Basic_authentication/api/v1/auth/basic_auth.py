#!/usr/bin/env python3
"""Basic Authentication Module
"""
from api.v1.auth.auth import Auth
import base64
import binascii
from typing import Tuple, TypeVar
from models.user import User


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
            decoded_msg = decoded_msg.decode("utf-8")
        except binascii.Error:
            return None
        except UnicodeDecodeError:
            return None
        return decoded_msg

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

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Gets User object
        Returns:
            TypeVar(User): User object
        """
        if not user_email or type(user_email) != str:
            return None
        if not user_pwd or type(user_pwd) != str:
            return None
        users = User.search({"email": user_email})
        if not users:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves te current user
        Returns:
            TypeVar(User): User object
        """
        auth_value =  self.authorization_header(request)
        value = self.extract_base64_authorization_header(auth_value)
        decoded = self.decode_base64_authorization_header(value)
        username, password = self.extract_user_credentials(decoded)
        user = self.user_object_from_credentials(username, password)
        return user
