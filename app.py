from flask import Flask, session
from os import environ
from flask_wtf import CSRFProtect
import scripts.utilities.endpoints as endpoint

app = Flask(__name__, template_folder = 'templates')

app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['MAIL_SERVER'] = environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = environ.get('MAIL_PORT')
app.config['MAIL_DEFAULT_SENDER'] = environ.get('MAIL_DEFAULT_SENDER')

# ------------------ #
# View Endpoints
# ------------------ #

app.add_url_rule('/', view_func = endpoint.index, methods = ['GET'])
app.add_url_rule('/logout', view_func = endpoint.logout, methods = ['GET'])
app.add_url_rule('/admin', view_func = endpoint.admin, methods = ['GET'])
app.add_url_rule('/docs', view_func = endpoint.home, methods = ['GET'])

# ------------------ #
# REST API Endpoints
# ------------------ #

app.add_url_rule('/login', view_func = endpoint.login, methods = ['POST'])
app.add_url_rule('/users', view_func = endpoint.users, methods = ['GET', 'POST'])
app.add_url_rule('/users/<id>', view_func = endpoint.user, methods = ['GET', 'PATCH'])

app.add_url_rule('/documents', view_func = endpoint.documents, methods = ['GET', 'POST'])
app.add_url_rule('/documents/<id>', view_func = endpoint.document, methods = ['GET', 'PATCH'])

# ------------------ #
# Miscellaneous
# ------------------ #

# Perform other post-request functionalities.
app.after_request(endpoint.finalResponseTouches)

# Add CSRF protection.
csrf = CSRFProtect()
csrf.init_app(app)

# For testing purposes when generating encrypted password:
app.add_url_rule('/passgen', view_func = endpoint.passgen, methods = ['GET'])