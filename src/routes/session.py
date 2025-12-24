from flask import Blueprint, request
from app import app
import time


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
    if request.headers.get('Content-Type') == 'application/json':
        data = request.get_json()
        name = data['name']
        password = data['password']
        expires_in = data['expires_in']
        is_live = data['is_live']
    else:
        name = request.form.get('name')
        password = request.form.get('password')
        expires_in = request.form.get('expires_in')  # int: number of hours
        is_live = bool(request.form.get('is_live'))

    expires_at = int(time.time()) + 3600  # default 1 hour expiry

    try:
        if expires_in:
            expires_in = int(expires_in)
            expires_at = int(time.time()) + (expires_in*60*60)
    except ValueError:
        return ("Bad Request", 400)

    if name is None or password is None:
        return ("Bad Request", 400)

    session_id = app.session_service.create_session(name,
                                                    password,
                                                    expires_at,
                                                    is_live)
    ama_url = f"{app.base_url}/sessions/{session_id}"

    return {
        "ama_url": ama_url
    }


@session_blueprint.get("/sessions/<session_id>")
def get_session(session_id: str):
    """
    get all your ama questions answered and unanswered
    if provided auth header using 'basic' strategy with ama session password
    ```
      authorization: basic <session-password>
    ```
    it will return all the unanswered questions too for the owner
    """
    authorization_header = request.headers.get('Authorization')
    password = authorization_header.removeprefix(
        'Basic ') if authorization_header else None
    res = app.session_service.get_session(
        session_id, password or None)
    if res is None:
        return ("Not Found", 404)
    session, questions = res
    return {
        'name': session.name,
        'is_live': session.is_live,
        'questions': questions,
    }
