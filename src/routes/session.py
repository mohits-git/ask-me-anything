from flask import Blueprint, request
from app import session_service, base_url


session_blueprint = Blueprint('session', __name__, url_prefix='/api')


@session_blueprint.post("/sessions")
def create_session():
    """
    POST /sessions to create a new AMA session
    expected request json body:
    ```
    {
      name: str,
      password: str
    }
    ```
    """
    # TODO: json vs form
    # data = request.get_json()
    name = request.form.get('name')
    password = request.form.get('password')
    if name is None or password is None:
        return ("Bad Request", 400)
    session_id = session_service.create_session(name, password)
    ama_url = f"{base_url}/sessions/{session_id}"
    return {
        "ama_url": ama_url
    }


@session_blueprint.get("/sessions/<session_id>")
def get_session(session_id: str):
    """
    get all your ama questions answered and unanswered
    if provided authorization header using 'basic' strategy with ama session password
    ```
      authorization: basic <session-password>
    ```
    it will return all the unanswered questions too for the owner
    """
    authorization_header = request.headers.get('Authorization')
    password = authorization_header.removeprefix(
        'Basic ') if authorization_header else None
    session, questions = session_service.get_session(
        session_id, password or None)
    return {
        'name': session.name,
        'questions': questions
    }
