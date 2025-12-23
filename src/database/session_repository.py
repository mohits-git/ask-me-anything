from database.connection import DatabaseConnection
from models import Session
import time


class SessionRepository:
    def __init__(self, db_uri: str) -> None:
        self._db_uri = db_uri
        self._create_session_table()

    def _create_session_table(self) -> None:
        with DatabaseConnection(self._db_uri) as connection:
            cursor = connection.cursor()
            query = "CREATE TABLE IF NOT EXISTS sessions(id TEXT PRIMARY KEY, name TEXT NOT NULL, password_hash TEXT NOT NULL, expires_at INTEGER, is_live BOOLEAN NOT NULL DEFAULT 0)"
            cursor.execute(query)

    def create_session(self, session: Session) -> None:
        with DatabaseConnection(self._db_uri) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO sessions VALUES(?, ?, ?, ?, ?)"
            cursor.execute(
                query,
                (
                    session.id,
                    session.name,
                    session.password_hash,
                    session.expires_at,
                    session.is_live,
                ))

    def find_session_by_id(self, session_id: str) -> Session | None:
        with DatabaseConnection(self._db_uri) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM sessions WHERE id = ?"
            cursor.execute(query, (session_id,))
            result = cursor.fetchone()
            if result is None:
                return None
            return Session(*result[:4], is_live=bool(result[4]))

    def expire_session(self, session_id) -> None:
        with DatabaseConnection(self._db_uri) as connection:
            cursor = connection.cursor()
            current_time = time.time() - 1
            query = "UPDATE sessions SET expires_at = ? WHERE id = ?"
            cursor.execute(query, (current_time, session_id))
