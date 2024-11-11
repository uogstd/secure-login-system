# backend/app/services/auth_service.py
from datetime import datetime, timedelta
import jwt
from app.models.user import User
from flask import current_app
from pymongo import MongoClient
import os

class AuthService:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client.secure_login_db
        self.users = self.db.users

    def create_or_update_user(self, user_info, oauth_provider):
        user = self.users.find_one({'email': user_info['email']})
        if not user:
            user = User(
                email=user_info['email'],
                name=user_info['name'],
                oauth_provider=oauth_provider
            )
            self.users.insert_one(user.to_dict())
        return user

    def generate_token(self, user_email):
        return jwt.encode(
            {
                'email': user_email,
                'exp': datetime.utcnow() + timedelta(hours=24)
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    def validate_token(self, token):
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            return self.users.find_one({'email': data['email']})
        except:
            return None