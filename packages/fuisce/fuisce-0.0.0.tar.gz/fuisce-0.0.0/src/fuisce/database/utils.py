"""
Tools for connecting to and working with the SQLite database.
"""
from functools import wraps

from flask import current_app


def db_transaction(func):
    """A decorator denoting the wrapped function as a database transaction."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        with current_app.db.session.begin():
            return func(*args, **kwargs)

    return wrapper
