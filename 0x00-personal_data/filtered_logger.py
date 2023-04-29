#!/usr/bin/env python3
"""Module containing a function that obfuscate a string.

"""
from typing import List
import re
import logging

PII_FIELDS = ("name", "email", "phone", "ssn", "ip")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscates a selected fields in a string
    """
    for field in fields:
        message = re.sub(f"{field}=.*?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Returns an obfuscated version of the log record"""
        message = super().format(record)
        redacted = filter_datum(self.fields, self.REDACTION,
                                  message, self.SEPARATOR)
        return redacted


def get_logger() -> logging.Logger:
    """Creates a logger object"""
    logger = logging.getLogger("user_data")
    logger.propagate = False
    logger.setLevel(logging.INFO)

    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger
