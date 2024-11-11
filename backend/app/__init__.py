from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.routes.auth import auth_bp, main_bp  # Import both auth and main blueprints
from app.routes.auth import configure_oauth  # Import configure_oauth function

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)  # Load your configurations directly into `app.config`
    
    # Configure OAuth directly with app.config
    configure_oauth(app)
    
    # Initialize CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')  # URL prefix for auth routes
    app.register_blueprint(main_bp)  # No prefix for the main route, handles the root path
    
    return app
