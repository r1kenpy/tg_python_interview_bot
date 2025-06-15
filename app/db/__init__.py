from .db import get_connection, WorkingWithDB

cur = WorkingWithDB()

__all__ = ["get_connection", "WorkingWithDB"]
