from app import app
from flask_socketio import (
    SocketIO,
    emit,
    join_room,
    leave_room,
    close_room,
    disconnect
)


def register_connection_events(socketio: SocketIO):
    """
    Registers the connection events to the socketio instance
    """
    @socketio.on('connect')
    def on_connect():
        pass

    @socketio.on('disconnect')
    def on_disconnect():
        pass

    @socketio.on('join')
    def on_join(data):
        session_id = None
        password = None
        try:
            session_id = data['session_id']
            password = data['password']
            if password == '':
                password = None
        except KeyError:
            password = None

        if not session_id:
            emit('error', {'message': 'Bad Request'}, broadcast=False)
            return disconnect()

        if not app.session_service.is_session_live(session_id):
            emit('error', {'message': 'Invalid Session'}, broadcast=False)
            return disconnect()

        if password:
            if not app.session_service.is_session_owner(session_id, password):
                emit('error', {'message': 'Invalid Password'}, broadcast=False)
                return disconnect()
            else:
                join_room(f"{session_id}-owner")

        join_room(session_id)

    @socketio.on('leave')
    def on_leave(data):
        session_id = None
        password = None
        try:
            session_id = data['session_id']
            password = data['password']
        except KeyError:
            password = None

        if not session_id:
            emit('error', {'message': 'Bad Request'}, broadcast=False)
            return disconnect()

        if app.session_service.is_session_owner(session_id, password):
            close_room(f"{session_id}-owner")
            return

        leave_room(session_id)
