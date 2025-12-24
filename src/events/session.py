from app import app
from flask_socketio import (
    SocketIO,
    close_room,
    emit
)


def register_session_events(socketio: SocketIO):
    """
    Registers the session resource events to the socketio instance
    """

    @socketio.on('post-question')
    def post_question(data):
        session_id = data['session_id']
        question = data['question']

        question_id = app.questions_service.create_question(
            session_id=session_id,
            question=question)

        emit('new-question',
             {'question_id': question_id, 'question': question},
             to=f"{session_id}-owner")
        return question_id

    @socketio.on('post-answer')
    def post_answer(data):
        session_id = data['session_id']
        password = data['password']
        question_id = data['question_id']
        answer = data['answer']
        question = data['question']

        try:
            app.questions_service.submit_answer(
                password,
                question_id,
                answer
            )
        except Exception:
            return False

        emit('new-question',
             {
                 'question_id': question_id,
                 'question': question,
                 'answer': answer,
             },
             to=session_id)
        return True

    @socketio.on('end-session')
    def end_session(data):
        session_id = data['session_id']
        password = data['password']

        ended = app.session_service.end_session(session_id, password)

        if not ended:
            return False

        emit('close', {'message': 'closed'}, to=session_id)
        close_room(session_id)
        close_room(f"{session_id}-owner")
