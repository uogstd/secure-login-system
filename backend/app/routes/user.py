# backend/app/routes/user.py
from flask import Blueprint, jsonify
from app.utils.decorators import token_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile')
@token_required
def get_profile(current_user):
    user_data = {
        'email': current_user['email'],
        'name': current_user['name'],
        'oauth_provider': current_user['oauth_provider']
    }
    return jsonify(user_data)