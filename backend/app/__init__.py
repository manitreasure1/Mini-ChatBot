
from flask import Flask
from app.routes import user_bp, chat_bp
from app.config import Config
from app.extensions import (db,
                            migrate,
                            bcrypt,
                            cors, mail,
                            swagger,
                            jwt_manager,
                            socketio, limiter,
                            compress, cache)


config = Config() # type: ignore

def create_app():
    app = Flask(__name__)

    app.config.from_object(config)

 
    mail.init_app(app)
    cache.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt_manager.init_app(app)
    swagger.init_app(app)
    socketio.init_app(app, cors_allowed_origins='*', logger=True, engineio_logger=True)
    limiter.init_app(app)
    compress.init_app(app)
    cors.init_app(
        app,
        resources={
            r"/api/*": {"origins": "*"}
            }, 
            allow_headers=['Content-Type', 'Authorization'],
            methods=['GET', 'POST', 'PUT', 'DELETE'],
            max_age=3600
            )


    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(chat_bp, url_prefix='/api/chats')

    return app



