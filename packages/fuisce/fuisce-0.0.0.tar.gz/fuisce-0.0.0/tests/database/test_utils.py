"""Tests for utility functions."""
from sqlalchemy import select
from sqlalchemy.sql.expression import func

from fuisce.database.utils import db_transaction
from fuisce.testing.helpers import transaction_lifetime

from testing_helpers import Entry


@transaction_lifetime
def test_transaction_decorator(client_context, app):
    # Define a function that uses the transaction generator to commit an action
    @db_transaction
    def execute_database_transaction(app, x, y):
        entry = Entry(x=x, y=y, user_id=1)
        app.db.session.add(entry)

    x, y = 5, "fifty"
    execute_database_transaction(app, x, y)
    # Ensure that the transaction was actually added
    query = select(func.count(Entry.x)).where(Entry.y == y)
    assert app.db.session.execute(query).scalar() == 1
