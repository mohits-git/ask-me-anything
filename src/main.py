from flask import Flask

import routes


def main():
    app = Flask(__name__)
    routes.register(app)
    return app


def run():
    app = main()
    app.run()


if __name__ == '__main__':
    run()
