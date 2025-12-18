from .connection import DatabaseConnection


class QuestionsRepository:
    def __init__(self, db_uri: str) -> None:
        self.db_uri = db_uri
        self._create_questions_table()

    def _create_questions_table(self):
        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            cursor = connection.execute("PRAGMA foreign_keys = ON")
            query = "CREATE TABLE IF NOT EXISTS questions(id TEXT PRIMARY KEY, session_id TEXT NOT NULL, question TEXT NOT NULL, answer TEXT, FOREIGN KEY(session_id) REFERENCES sessions(id))"
            cursor.execute(query)

    def create_question(self, question_id, session_id, question):
        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            query = "INSERT INTO questions(id, session_id, question) VALUES (?, ?, ?)"
            cursor.execute(query, (question_id, session_id, question))

    def answer_question(self, question_id, answer):
        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            query = "UPDATE questions SET answer = ? WHERE id = ?"
            cursor.execute(query, (answer, question_id))

    def find_all_questions(self, session_id) -> list[dict]:
        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM questions WHERE session_id = ?"
            cursor.execute(query, (session_id,))
            questions = [
                {
                    'id': result[0],
                    'session_id': result[1],
                    'question': result[2],
                    'answer': result[3]
                }
                for result in cursor.fetchall()
            ]
            return questions

    def find_question_by_id(self, question_id) -> dict:
        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM questions WHERE id = ?"
            cursor.execute(query, (question_id,))
            result = cursor.fetchone()
            question = {
                'id': result[0],
                'session_id': result[1],
                'question': result[2],
                'answer': result[3]
            }
            return question
