from scripts.classes.controllers.BaseController import BaseController
from scripts.classes.models.UserModel import UserModel
from scripts.utilities.passwordHash import PasswordHash as passHash
from flask import jsonify

class LoginController(BaseController):

    __user = {}

    def __init__(self):
        super().__init__()
        self.__user = UserModel()

    def doLogin(self):
        checkInputs = self.__validateInputs()
        if checkInputs['result'] == False:
            return jsonify(checkInputs)

        checkLogin = self.__checkLogin()
        if checkLogin['result'] == False:
            return jsonify(checkLogin)

        self.__startSession(checkLogin.pop('userDetails'))
        return jsonify(checkLogin)

    def __validateInputs(self):
        if self._inputs['username'] == '':
            return {'result': False, 'title': 'Invalid Credential', 'message': 'Please enter your username.'}

        if self._inputs['password'] == '':
            return {'result': False, 'title': 'Invalid Credential', 'message': 'Please enter your password.'}

        return {'result': True}

    def __checkLogin(self):
        userDetails = self.__user.getUserBy('username', self._inputs['username'])
        if userDetails == None:
            return {'result': False, 'title': 'Invalid Username', 'message': 'User not found.'}

        if passHash.decrypt(userDetails['password']) != self._inputs['password']:
            return {'result': False, 'title': 'Invalid Password', 'message': 'Password is incorrect.'}

        if userDetails['status'] == 'inactive':
            return {'result': False, 'title': 'Account Deactivated', 'message': 'Your account is disabled.'}

        return {'result': True, 'userDetails': userDetails}

    def __startSession(self, userDetails):
        keysToUnset = ['address', 'contact_num', 'email', 'password', 'status']
        for key in keysToUnset:
            del userDetails[key]

        self._auth.setSession(**userDetails)