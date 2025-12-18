from database.connection import DatabaseConnection
from models import Session


class SessionRepository:
    def __init__(self, db_uri: str) -> None:
        self._db_uri = db_uri
        self._create_session_table()

    def _create_session_table(self) -> None:
        with DatabaseConnection(self._db_uri) as connection:
            cursor = connection.cursor()
            query = "CREATE TABLE IF NOT EXISTS sessions(id TEXT PRIMARY KEY, name TEXT NOT NULL, password_hash TEXT NOT NULL)"
            cursor.execute(query)

    def create_session(self, session: Session) -> None:
        with DatabaseConnection(self._db_uri) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO sessions VALUES(?, ?, ?)"
            cursor.execute(
                query, (session.id, session.name, session.password_hash))

    def find_session_by_id(self, id) -> dict:
        with DatabaseConnection(self._db_uri) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM sessions WHERE id = ?"
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            return {
                'id': result[0],
                'name': result[1],
                'password_hash': result[2],
            }
