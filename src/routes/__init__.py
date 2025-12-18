from flask import Flask

from .session import session_blueprint
from .questions import questions_blueprint


def register(app: Flask) -> None:
    app.register_blueprint(session_blueprint)
    app.register_blueprint(questions_blueprint)
