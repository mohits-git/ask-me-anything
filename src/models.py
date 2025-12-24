from dataclasses import dataclass


@dataclass
class Session:
    id: str
    name: str
    password_hash: str
    expires_at: int
    is_live: bool


@dataclass
class Question:
    id: str
    session_id: str
    question: str
    answer: str | None
