#!/usr/bin/env python3
"""Module containing a function that obfuscate a string.

"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str,
                 seperator: str) -> str:
    """Obfuscates a string

    """
    for field in fields:
        message = re.sub(f"{field}=.*?{seperator}",
                         f"{field}={redaction}{seperator}", message)
    return message
