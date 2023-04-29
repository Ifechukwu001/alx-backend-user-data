#!/usr/bin/env python3
"""Encryptions and Passwords :)"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a hashed salted password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if a hash was generated from a password"""
    return bcrypt.checkpw(password.encode(), hashed_password)
