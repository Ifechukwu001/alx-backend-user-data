#!/usr/bin/env python3
"""Module containing a function that obfuscate a string.

"""
from typing import List
import re
import logging
import os
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Creates a Database connection object"""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD")
    host = os.getenv("PERSONAL_DATA_DB_HOST")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    connection = mysql.connector.connect(
                                            user=username,
                                            password=password,
                                            host=host,
                                            database=database
                                        )
    return connection


def main():
    """Entry point of the function"""
    connection = get_db()
    cursor = connection.cursor()
    log = get_logger()

    quer = cursor.execute("SELECT * FROM users;")

    for name, email, phone, ssn, password, ip, last_login, user_agent in quer:
        log.info(f"name={name}; email={email}; phone={phone}; ssn={ssn};"
                 f" password={password}; ip={ip}; last_login={last_login};"
                 f" user_agent={user_agent};"
                )


if __name__ == "__main__":
    main()
