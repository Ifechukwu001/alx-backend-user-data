#!/usr/bin/env pythpn3
"""Encryptions and Passwords :)"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a hashed salted password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
