
import logging
from typing import Any
from app.schemas import LoginUser, UpdateUser, CreateUser, SendMessage
from app.models import Users, ChatMessage
from sqlalchemy import select
from flask import request, jsonify
from app.extensions import bcrypt,db, jwt_manager
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, get_current_user
from app.redis import jwt_redis_block_list
from werkzeug.exceptions import  NotFound, Forbidden
from uuid import UUID
from app.chat import chatbot
from app.utils import text_correction




@jwt_manager.user_lookup_loader
def users_lookup_callback(jwt_header, jwt_data: dict[Any, Any]):
    try:
        identity = jwt_data['sub']
        user_id_uuid = UUID(identity)
        return Users.get_user_by_id(user_id_uuid)
    except Exception as e:
        logging.exception(e)


@jwt_manager.token_in_blocklist_loader
def check_revoked_token(jwt_header, jwt_data: dict[Any, Any]):
    user_id = jwt_data['jti']
    token_in_redis = jwt_redis_block_list.get(str(user_id))
    return token_in_redis is not None    



class UserServices:
    def get_user_by_email(self, user_email: str):
        user = db.session.execute(select(Users).where(Users.email == user_email))
        return user.scalar_one_or_none()       
        

    def existing_user(self, user_email: str):
            ex_user = self.get_user_by_email(user_email)
            return ex_user

    
    def update_user(self, current_user: Any):
            user_data = request.get_json()
            user_to_update = UpdateUser(**user_data)
            user_db =  self.get_user_by_email(current_user.email)
            if not user_db:
                raise NotFound(description='user not found')
            user_update_data = user_to_update.model_dump(exclude_unset=True)
            print(user_data)
            for key, value in user_update_data.items():
                setattr(user_db, key, value)
            db.session.commit()
            db.session.refresh(user_db)
            


    def remove_user(self, user_id: str):
        user_db = self.get_user_by_email(user_id)
        if not user_db:
            raise NotFound(description='user not found')
        db.session.delete(user_db)
        db.session.commit()

    def user_history(self, user_id: str):
        history = db.session.execute(select(ChatMessage).where(ChatMessage.user_id == user_id))
        return history.scalars()        


user_service = UserServices()


class AuthServices:
    def register_new_user(self):
        user_data = request.get_json()
    
        user = CreateUser(**user_data)
        existing_user = user_service.existing_user(user.email)
        if existing_user:
            raise Forbidden(description='User Already Exist!')
        password_hashed = bcrypt.generate_password_hash(user.password)
        user_create_db = Users(
            firstname=user.firstname, # type: ignore
            lastname=user.lastname, # type: ignore
            username=user.email.split("@")[0], # type: ignore
            email=user.email, # type: ignore
            password_hash=password_hashed  # type: ignore
        )
        db.session.add(user_create_db)
        db.session.commit()
        db.session.refresh(user_create_db)
        return jsonify({"msg":"User Created Successfully!"})
        

    def login_user(self):
        user_data = request.get_json()
        user = LoginUser(**user_data)
        login_user = user_service.get_user_by_email(user.email)

        if login_user is None:
            raise Forbidden(description='Invalid email or password')
        if not bcrypt.check_password_hash(login_user.password_hash, user.password):
            raise Forbidden(description='Invalid email or password')
        payload = login_user.user_id
        access_token = create_access_token(identity=payload, fresh=True)
        refresh_token = create_refresh_token(identity=payload)
        response = jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,
        })
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response
    

    
            


class ChatServive:
    def send_message(self):
        message_json = request.get_json()
        message_validation = SendMessage(**message_json)
        message = str(message_validation).strip()
        clean_txt = text_correction(message)

        resopnse = chatbot(clean_txt)
        
        # user_id = get_current_user()
        # if user_id:
        #     user_history =ChatMessage(
        #         message=message,  # type: ignore
        #         response=response, # type: ignore
        #         user_id=user_id # type: ignore
        #     )
        #     db.session.add(user_history)
        #     db.session.commit()
        #     db.session.refresh(user_history)
        return resopnse

