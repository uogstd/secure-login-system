# backend/app/models/user.py
from datetime import datetime

class User:
    def __init__(self, email, name, oauth_provider):
        self.email = email
        self.name = name
        self.oauth_provider = oauth_provider
        self.created_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            'email': self.email,
            'name': self.name,
            'oauth_provider': self.oauth_provider,
            'created_at': self.created_at
        }