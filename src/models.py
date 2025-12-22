from dataclasses import dataclass


@dataclass
class Session:
    id: str
    name: str
    password_hash: str
    expires_at: int


@dataclass
class Question:
    id: str
    session_id: str
    question: str
    answer: str | None
