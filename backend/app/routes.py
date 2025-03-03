from flask import Blueprint, jsonify, make_response
from flasgger import swag_from
from app.services import AuthServices, UserServices, ChatServive
from app.redis import jwt_redis_block_list
from flask_jwt_extended import (create_access_token,
                                get_jwt_identity,
                                jwt_required,
                                get_current_user,
                                get_jwt)
from app.config import Config
from werkzeug.exceptions import HTTPException
from app.extensions import socketio, cache
from flask_socketio import emit




user_bp = Blueprint('user', __name__)
chat_bp = Blueprint('chat', __name__)

config = Config() # type: ignore
auth_service = AuthServices()
user_service = UserServices()
chat_service = ChatServive()

@user_bp.route("/register/", methods=['POST'])
@swag_from({
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "firstname": {
                        "type": "string",
                        "example": "Ava"
                    },
                    "lastname": {
                        "type": "string",
                        "example": "Believe"
                    },
                    "email": {
                        "type": "string",
                        "example": "ex@email.com"},
                    "password": {
                        "type": "string",
                        "example": "password@123"
                    }
                }
            }
        }
    ],
    "responses": {
        201: {
            "description": "User registered successfully",
            "examples": {
                "application/json": {
                    "message": "User registered successfully"
                }
            }
        },
        400: {
            "description": "Invalid input",
            "examples": {
                "application/json": {
                    "message": "Invalid input"
                }
            }
        }
    }
})
def register():
    try:
        new_user = auth_service.register_new_user()
        return make_response(jsonify(new_user.get_json()), 201)
    except HTTPException as e:
        raise e


@user_bp.route('/login/', methods=['POST'])
@swag_from({
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "example": "ex@email.com"},
                    "password": {
                        "type": "string",
                        "example": "password@123"
                    }
                }
            }
        }
    ],
    "responses": {
        200: {
            "description": "User logged in successfully",
            "examples": {
                "application/json": {
                    "message": "User logged in successfully"
                }
            }
        }
    }
})
def login():
    try:
        login_user = auth_service.login_user()
        return login_user.get_json()
    except HTTPException as e:
        raise e

    
@user_bp.route('/refresh', methods=['POST'])
@swag_from({
    "responses": {
        200: {
            "description": "Token refreshed successfully",
            "examples": {
                "application/json": {
                    "message": "Token refreshed successfully"
                }
            }
        }
    }
})
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)


@user_bp.put('/update/')
@jwt_required(fresh=True)
def update_user_data():
    try:
        user_service.update_user(get_current_user())
        return make_response('', 204)
    except HTTPException as e:
        raise e


@user_bp.route('/logout', methods=['DELETE'])
@swag_from({
    "responses": {
        204: {
            "description": "User logged out successfully",
            "examples": {
                "application/json": {
                    "message": "User logged out successfully"
                }
            }
        }
    }
})
@jwt_required(fresh=True)
def logout():
    jti = get_jwt()['jti']
    jwt_redis_block_list.set(jti, 'true', ex=config.JWT_ACCESS_TOKEN_EXPIRES)
    return make_response("", 204)
    


"""
THE CHAT ROUTES
"""



@chat_bp.route('/send/', methods=['POST'])
@socketio.on('send_message')
@swag_from({
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "Hello"
                    }
                }
            }
        }
    ],
    "responses": {
        201: {
            "description": "Message sent successfully",
            "examples": {
                "application/json": {
                    "message": "Message sent successfully"
                }
            }
        },
        400: {
            "description": "Invalid input",
            "examples": {
                "application/json": {
                    "message": "Invalid input"
                }
            }
        }
    }
})
@jwt_required(optional=True)
def send_message():
    try:
        response = chat_service.send_message()
        return make_response(response, 200)
    except Exception as e:
       raise e


@cache.memoize(30)
@chat_bp.route("/chat-history")
def chat_history():
    try:
        user_id = get_current_user()
        user_history = user_service.user_history(user_id)
        return jsonify(user_history)
    except Exception as e:
        raise e
    


# @celery.task()
# def send_mail():
#     pass
    
    