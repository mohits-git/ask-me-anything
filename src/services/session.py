from database.questions_repository import QuestionsRepository
from database.session_repository import SessionRepository
from models import Question, Session
from utils.uuid_custom import generate_uuid
from utils.hashing_service import hash_password, verify_hashed_password


class SessionService:
    def __init__(
            self,
            session_repo: SessionRepository,
            questions_repo: QuestionsRepository,
    ):
        self._session_repo = session_repo
        self._questions_repo = questions_repo

    def create_session(self, name: str, password: str) -> str:
        password_hash = hash_password(password)
        id = generate_uuid()
        session = Session(id, name, password_hash)
        self._session_repo.create_session(session)
        return id

    def get_session(self, id: str, password: str | None) -> tuple[Session, list[Question]]:
        session_result = self._session_repo.find_session_by_id(id)
        session = Session(
            session_result['id'],
            session_result['name'],
            session_result['password_hash'])
        questions_result = self._questions_repo.find_all_questions(
            session_id=id)
        questions = [
            Question(res['id'], res['session_id'],
                     res['question'], res['answer'])
            for res in questions_result
        ]
        if password is not None and verify_hashed_password(password, session.password_hash):
            session.password_hash = ''
            return (session, questions)
        session.password_hash = ''
        questions = [
            q for q in questions if q.answer is not None
        ]
        return (session, questions)

    def is_session_owner(self, session_id, password) -> bool:
        session_result = self._session_repo.find_session_by_id(session_id)
        if verify_hashed_password(password, session_result['password_hash']):
            return True
        return False
