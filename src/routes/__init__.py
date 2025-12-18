from flask import Flask

from .session import session_blueprint
from .questions import questions_blueprint
from .pages import pages_blueprint


def register(app: Flask) -> None:
    app.register_blueprint(session_blueprint)
    app.register_blueprint(questions_blueprint)
    app.register_blueprint(pages_blueprint)
