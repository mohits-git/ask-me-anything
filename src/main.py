import os
from flask import Flask
from flask_socketio import SocketIO

import events
import routes


def create_flask_app() -> Flask:
    template_dir = os.path.abspath('./templates')
    flask_app = Flask(__name__, template_folder=template_dir)
    routes.register(flask_app)
    return flask_app


def create_socketio():
    socketio = SocketIO()
    events.register_events(socketio)
    return socketio


def run():
    app = create_flask_app()
    socketio = create_socketio()
    socketio.init_app(app)
    socketio.run(app, port=5000, debug=True)


if __name__ == '__main__':
    run()
