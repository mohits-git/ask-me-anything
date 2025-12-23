from flask import Blueprint, request
from app import app


questions_blueprint = Blueprint('question', __name__, url_prefix='/api')


@questions_blueprint.post("/questions")
def create_question():
    """
    POST /questions to create a new question in AMA session
    expected request json body:
    ```
    {
      session_id: str,
      question: str
    }
    ```
    """
    session_id = request.form.get("session_id")
    question = request.form.get("question")
    if request.headers.get('Content-Type') == 'application/json':
        data = request.get_json()
        session_id = data['session_id']
        question = data['question']
    if not session_id or not question:
        return ("Bad Request", 400)
    question_id = app.questions_service.create_question(
        session_id, question)
    return {'question_id': question_id}


@questions_blueprint.patch("/questions/<question_id>")
def answer_question(question_id):
    """
    Post the Answer to the question asked in your particular AMA session
    Requires Authorization header using 'Basic' strategy with AMA session password
    ```
      Authorization: Basic <session-password>
    ```
    """
    data = request.get_json()
    authorization_header = request.headers.get('Authorization')
    password = authorization_header.removeprefix(
        'Basic ') if authorization_header else None
    if not password:
        return ("Invalid Password", 401)
    try:
        app.questions_service.submit_answer(
            password, question_id, data['answer'])
    except Exception as e:
        return (str(e), 500)
    return 'Ok'
