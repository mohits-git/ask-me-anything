from database.questions_repository import QuestionsRepository
from database.session_repository import SessionRepository
from models import Question, Session
from utils.uuid import generate_uuid
from utils.hashing_service import verify_hashed_password


class QuestionsService:
    def __init__(
            self,
            questions_repo: QuestionsRepository,
            session_repo: SessionRepository,
    ):
        self._questions_repo = questions_repo
        self._session_repo = session_repo

    def create_question(self, session_id: str, question: str) -> str:
        question_id = generate_uuid()
        self._questions_repo.create_question(question_id, session_id, question)
        return question_id

    def submit_answer(self, password: str, question_id: str, answer: str):
        question_exists = self._questions_repo.find_question_by_id(question_id)
        question_exists = Question(**question_exists)
        session_exists = self._session_repo.find_session_by_id(question_exists.session_id)
        session_exists = Session(**session_exists)
        if not verify_hashed_password(password, session_exists.password_hash):
            raise Exception("Forbidden")
        self._questions_repo.answer_question(question_id, answer)
