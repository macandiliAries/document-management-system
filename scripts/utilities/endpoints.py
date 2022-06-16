from flask import render_template, redirect, request, jsonify
from flask_wtf import csrf
from functools import wraps
from scripts.utilities.utils import requestDataToJsonObject, requestDataToJsonString
from scripts.utilities.sessionHandler import SessionHandler
from scripts.utilities.passwordHash import PasswordHash as passHash
from scripts.classes.controllers.LoginController import LoginController
from scripts.classes.controllers.UserController import UserController
from scripts.classes.controllers.DocumentController import DocumentController
from scripts.classes.controllers.DocumentTypeController import DocumentTypeController
import time
auth = SessionHandler()

# ------------------ #
# Wrappers
# ------------------ #
def login_required(f):
    
    @wraps(f)
    def wrap(*args, **kwargs):
        if auth.isLoggedIn() == False:
            return redirect('/')
        return f(*args, **kwargs)

    return wrap

# ------------------ #
# Login-Related Endpoints
# ------------------ #

def index():
    if auth.isLoggedIn() == False:
        return render_template('login.html', data = {'showNav': False})
    return redirect('/docs')

def login():
    return LoginController().doLogin()

def logout():
    auth.destroySession()
    return redirect('/')

# ------------------ #
# User-Related Endpoints
# ------------------ #

@login_required
def admin():
    return render_template('admin.html', users = requestDataToJsonString(UserController().getUsers()))

@login_required
def users():
    userController = UserController()

    if request.method == 'GET':
        return userController.getUsers()

    if request.method == 'POST':
        return userController.createUser()

@login_required
def user(id):
    userController = UserController()

    if request.method == 'GET':
        return userController.getUserDetails(id)

    if request.method == 'PATCH':
        if request.get_json()['action'] not in ['updatePassword', 'updateUserDetails']:
            return userController.triggerUserTableActions(id)

        return userController.updateUserDetails(id)

# ------------------ #
# Document-Related Endpoints
# ------------------ #

@login_required
def home():
    return render_template('docs.html', viewData = {
        'documents'     : requestDataToJsonString(DocumentController().getDocuments()),
        'documentTypes' : requestDataToJsonObject(DocumentTypeController().getDocumentTypes())
    })

@login_required
def documents():
    documentController = DocumentController()

    if request.method == 'GET':
        return documentController.getDocuments()

    if request.method == 'POST':
        return documentController.createDocument()

@login_required
def document(id):
    documentController = DocumentController()

    if request.method == 'GET':
        return documentController.getDocumentDetails(id)
    
    if request.method == 'PATCH':
        if request.get_json()['operation'] in ['submitDocumentForReview', 'approveDocument', 'denyDocument', 'tagDocumentForRevision', 'deleteDocument']:
            return documentController.triggerDocsTableActions(id)

        return documentController.updateDocument(id)

# ------------------ #
# Miscellaneous Endpoints
# ------------------ #

def finalResponseTouches(response):
    # Set current time in milliseconds on the session variables (for cache busting).
    SessionHandler().setSession(timeInMs = round(time.time() * 1000))

    if request.method != 'GET':
        rawResponse = response.get_json()
        rawResponse['new_token'] = csrf.generate_csrf()
        response = jsonify(rawResponse)

    return response

def passgen():
    # Sample Usage: http://localhost/passgen?pass=admin
    return passHash.encrypt(request.args.get('pass'))