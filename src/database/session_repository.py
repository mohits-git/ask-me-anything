from database.connection import DatabaseConnection
from models import Session


class SessionRepository:
    def __init__(self, db_uri: str) -> None:
        self._db_uri = db_uri
        self._create_session_table()

    def _create_session_table(self) -> None:
        with DatabaseConnection(self._db_uri) as connection:
            cursor = connection.cursor()
            query = "CREATE TABLE IF NOT EXISTS sessions(id TEXT PRIMARY KEY, name TEXT NOT NULL, password_hash TEXT NOT NULL, expires_at INTEGER)"
            cursor.execute(query)

    def create_session(self, session: Session) -> None:
        with DatabaseConnection(self._db_uri) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO sessions VALUES(?, ?, ?, ?)"
            cursor.execute(
                query,
                (session.id, session.name, session.password_hash, session.expires_at))

    def find_session_by_id(self, id) -> Session | None:
        with DatabaseConnection(self._db_uri) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM sessions WHERE id = ?"
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            if result is None:
                return None
            return Session(*result)
