from flask import Blueprint, request, jsonify, current_app
from authlib.integrations.flask_client import OAuth
from app.services.auth_service import AuthService

# Define blueprints for auth and main routes
auth_bp = Blueprint('auth', __name__)
main_bp = Blueprint('main', __name__)

oauth = OAuth()
auth_service = AuthService()

def configure_oauth(app):
    # Initialize OAuth with the app context
    oauth.init_app(app)
    # Register OAuth provider with config values from the app context
    oauth.register(
        name='google',
        client_id=app.config.get('GOOGLE_CLIENT_ID'),
        client_secret=app.config.get('GOOGLE_CLIENT_SECRET'),
        access_token_url='https://accounts.google.com/o/oauth2/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        client_kwargs={'scope': 'openid email profile'},
    )

@auth_bp.route('/google')
def google_auth():
    # Redirect to Google's OAuth authorization URL
    redirect_uri = current_app.config.get('REDIRECT_URI') or 'http://localhost:3000'
    return oauth.google.authorize_redirect(redirect_uri=redirect_uri)

@auth_bp.route('/google/callback')
def google_callback():
    # Obtain token and user info from Google
    token = oauth.google.authorize_access_token()
    resp = oauth.google.get('userinfo')
    user_info = resp.json()
    
    # Process user info with AuthService
    user = auth_service.create_or_update_user(user_info, 'google')
    token = auth_service.generate_token(user_info['email'])
    
    return jsonify({'token': token})

# Root route for the main blueprint
@main_bp.route('/')
def home():
    return "Hello, World!"  # This will display on the root page

# Handle the favicon.ico request to avoid 404 error
@main_bp.route('/favicon.ico')
def favicon():
    return '', 204  # Respond with no content (204 No Content)
