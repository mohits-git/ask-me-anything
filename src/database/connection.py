import sqlite3


class DatabaseConnection:
    def __init__(self, host="ama.db"):
        self.connection = None
        self.host = host

    def __enter__(self):
        conn = sqlite3.connect(self.host)
        self.connection = conn
        return conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection is None:
            return
        if not (exc_type or exc_val or exc_tb):
            self.connection.commit()
        self.connection.close()
