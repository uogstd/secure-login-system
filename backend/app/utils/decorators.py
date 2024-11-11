# backend/app/utils/decorators.py
from functools import wraps
from flask import request, jsonify
from app.services.auth_service import AuthService

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_service = AuthService()

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        current_user = auth_service.validate_token(token)
        if not current_user:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated