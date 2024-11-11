# backend/app/routes/__init__.py
"""
This module contains all the route blueprints for the application.
"""
from app.routes.auth import auth_bp
from app.routes.user import user_bp

__all__ = ['auth_bp', 'user_bp']