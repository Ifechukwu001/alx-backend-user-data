#!/usr/bin/env python3
"""Module containing the authentication
"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """Hashes a string password
    Returns:
        bytes: Hashed password
    """
    return hashpw(password.encode("utf-8"), gensalt())
