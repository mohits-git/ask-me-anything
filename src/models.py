from dataclasses import dataclass


@dataclass
class Session:
    id: str
    name: str
    password_hash: str


@dataclass
class Question:
    id: str
    session_id: str
    question: str
    answer: str | None
