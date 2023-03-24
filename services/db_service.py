import sqlite3


class DB:
    def __init__(self, database="taskstest.db") -> None:
        self.database = database

    def connect(self):
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.conn.close()


db = DB()


def create_table_if_not_exists():
    db.cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            deadline INTEGER,
            priority INTEGER,
            status INTEGER,
            created INTEGER,
            updated INTEGER)"""
    )
