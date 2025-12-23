from dataclasses import dataclass
from database.questions_repository import QuestionsRepository
from database.session_repository import SessionRepository
from services.questions import QuestionsService
from services.session import SessionService
import os


@dataclass
class App:
    _instance = None
    _initialized = False

    def __init__(self):
        if self._initialized:
            return
        # load envs
        _db_uri = os.getenv('DB_URI')
        if not _db_uri:
            _db_uri = "ama.db"

        _session_repo = SessionRepository(_db_uri)
        _questions_repo = QuestionsRepository(_db_uri)

        self.session_service = SessionService(
            _session_repo, _questions_repo)
        self.questions_service = QuestionsService(
            _questions_repo, _session_repo)
        self.base_url = "http://localhost:5000"
        self._initialized = True

    def __new__(cls, *args, **kwargs):
        print('new called')
        if cls._instance is None:
            cls._instance = super(App, cls).__new__(cls)
        return cls._instance


app = App()
