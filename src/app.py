from database.questions_repository import QuestionsRepository
from database.session_repository import SessionRepository
from services.questions import QuestionsService
from services.session import SessionService

_db_uri = "ama.db"
_session_repo = SessionRepository(_db_uri)
_questions_repo = QuestionsRepository(_db_uri)

base_url = "http://localhost:5000"
session_service = SessionService(_session_repo, _questions_repo)
questions_service = QuestionsService(_questions_repo, _session_repo)
