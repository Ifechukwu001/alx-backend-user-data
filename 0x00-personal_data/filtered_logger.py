#!/usr/bin/env python3
"""Module containing a function that obfuscate a string.

"""
from typing import List
import re
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Obfuscates a selected fieldsnin a string"""
    for field in fields:
        message = re.sub(f"{field}=.*?{seperator}",
                         f"{field}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List) -> None:
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Returns an obfuscated version of the log record"""
        message = record.getMessage()
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  message, self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
