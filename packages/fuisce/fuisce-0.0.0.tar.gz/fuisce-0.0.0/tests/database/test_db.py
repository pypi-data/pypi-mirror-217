"""Tests for the basic database objects."""


def test_database(app):
    assert "entries" in app.db.tables.keys()
