import os
from datetime import timedelta

from flask import Flask, render_template, request, session, redirect
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

from .models import db, User, SavedRestaurant
from .api.user_routes import user_routes
from .api.auth_routes import auth_routes
from .api.reservation_routes import reservation_routes
from .api.restaurant_routes import restaurant_routes
from .api.review_routes import review_routes
from .api.restaurant_manager_routes import restaurant_manager_routes
from  .api.admin_routes import admin_routes

from flask_mail import Mail



from .seeds import seed_commands
from .config import Config

app = Flask(__name__, static_folder='../front-end/build', static_url_path='/')

# Setup login manager
login = LoginManager(app)
login.login_view = 'auth.unauthorized'

mail = Mail()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# Tell flask about our seed commands
app.cli.add_command(seed_commands)

app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
Migrate(app, db)
mail.init_app(app)
CORS(app)
jwt = JWTManager(app)

# JWT secret key
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'super-secret-key')
# Add this:
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)  # Short token lifetime
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)    # Refresh token valid for 30 days


# Register Blueprints
app.register_blueprint(user_routes, url_prefix='/api/users')
app.register_blueprint(auth_routes, url_prefix='/api/auth')
app.register_blueprint(reservation_routes, url_prefix='/api/reservations')
app.register_blueprint(restaurant_routes, url_prefix='/api/restaurants')
app.register_blueprint(review_routes, url_prefix='/api/reviews')
app.register_blueprint(restaurant_manager_routes, url_prefix='/api')
app.register_blueprint(admin_routes)

# HTTPS redirect in production
@app.before_request
def https_redirect():
    if os.environ.get('FLASK_ENV') == 'production':
        if request.headers.get('X-Forwarded-Proto') == 'http':
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)

# CSRF token injection
@app.after_request
def inject_csrf_token(response):
    response.set_cookie(
        'csrf_token',
        generate_csrf(),
        secure=True if os.environ.get('FLASK_ENV') == 'production' else False,
        samesite='Strict' if os.environ.get(
            'FLASK_ENV') == 'production' else None,
        httponly=True)
    return response

# API Docs route
@app.route("/api/docs")
def api_help():
    """
    Returns all API routes and their doc strings
    """
    acceptable_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    route_list = { rule.rule: [[ method for method in rule.methods if method in acceptable_methods ],
                    app.view_functions[rule.endpoint].__doc__ ]
                    for rule in app.url_map.iter_rules() if rule.endpoint != 'static' }
    return route_list

# React fallback route
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_root(path):
    """
    This route will direct to the public directory in our
    react builds in the production environment for favicon
    or index.html requests
    """
    if path == 'favicon.ico':
        return app.send_from_directory('public', 'favicon.ico')
    return app.send_static_file('index.html')


@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')