# backend/app/utils/__init__.py
"""
This module contains utility functions and decorators.
"""
from app.utils.decorators import token_required

__all__ = ['token_required']