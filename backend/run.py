# backend/run.py
from app import create_app

app = create_app()

with app.app_context():
    # Any code that needs to access `current_app.config` can go here
    # For example, you could call any initialization functions here
    pass

if __name__ == '__main__':
    app.run(ssl_context="adhoc", debug=True)
