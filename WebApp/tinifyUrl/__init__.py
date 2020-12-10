from flask import Flask


def create_app():
    from tinifyUrl import service, frontend, redis
    app = Flask(__name__)

    # Initialize redis
    redis.init_app(app)

    app.register_blueprint(service.bp)
    app.register_blueprint(frontend.bp)
    return app
