"""Helper objects to improve modularity of tests."""
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

from fuisce.database import Model


class Entry(Model):
    __tablename__ = "entries"
    # Columns
    x = mapped_column(Integer, primary_key=True)
    y = mapped_column(String, nullable=False)
    user_id = mapped_column(Integer, nullable=False)
