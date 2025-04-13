from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flasgger import Swagger
from app.config import Config
from flask_compress import Compress
from flask_caching import Cache
from flask_mail import Mail

config = Config()  # type: ignore


mail =Mail()
cache =Cache()
compress = Compress()
cors = CORS()
db = SQLAlchemy()
bcrypt  = Bcrypt()
migrate = Migrate()
jwt_manager = JWTManager()
swagger = Swagger()
socketio = SocketIO(async_mode="gevent")
limiter = Limiter(get_remote_address,
                  storage_uri=config.REDIS_URL,
                  storage_options={'socket_connect_timeout': 30},
                  strategy="fixed-window"
                 )

