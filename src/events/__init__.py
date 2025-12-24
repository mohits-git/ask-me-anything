from flask_socketio import SocketIO

from events.session import register_session_events
from .connection import register_connection_events


def register_events(socketio: SocketIO):
    register_connection_events(socketio)
    register_session_events(socketio)
