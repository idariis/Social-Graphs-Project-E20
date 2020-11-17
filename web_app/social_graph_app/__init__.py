"""Initialize Flask app."""
from flask import Flask


def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__)

    with app.app_context():
        # Import parts of our core Flask app
        from . import routes

        # Import Dash application
        # I.e. embededing an app (Dash) within an app (Flask). 
        from plotlydash.dashboard import create_dashboard
        app = create_dashboard(app)

        return app