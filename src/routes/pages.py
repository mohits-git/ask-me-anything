from flask import Blueprint, render_template, request
from app import app


pages_blueprint = Blueprint('pages', __name__)


@pages_blueprint.route('/', methods=["GET"])
def home_page():
    return render_template('home.html')


@pages_blueprint.route('/sessions/<session_id>', methods=["GET"])
def session_page(session_id: str):
    owner = False

    password = request.args.get('password')

    if password and app.session_service.is_session_owner(session_id, password):
        owner = True

    res = app.session_service.get_session(session_id, password)
    if res is None:
        return ("Not Found", 404)

    session, questions = res

    if not session:
        return ("Not Found", 404)

    return render_template(
        'session.html',
        password=(password if owner else None),
        session=session,
        questions=questions)
