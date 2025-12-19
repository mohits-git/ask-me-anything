import os
from flask import Flask

import routes


def main():
    template_dir = os.path.abspath('./templates')
    app = Flask(__name__, template_folder=template_dir)
    routes.register(app)
    return app


def run():
    app = main()
    app.run()


if __name__ == '__main__':
    run()
