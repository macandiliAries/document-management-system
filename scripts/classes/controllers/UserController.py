from scripts.classes.controllers.BaseController import BaseController
from scripts.classes.models.UserModel import UserModel
from scripts.classes.services.UserValidation import UpdatePasswordValidation, CreateNewValidation, UpdateDetailsValidation
from scripts.utilities.passwordHash import PasswordHash as passHash
from flask import jsonify
import wtforms_json
wtforms_json.init() # Initialize WTForms using JSON values.

class UserController(BaseController):

    __userModel = {}

    def __init__(self):
        super().__init__()
        self.__userModel = UserModel()

    def getUsers(self):
        return jsonify(self.__userModel.getUsers())

    def getUserDetails(self, id):
        return jsonify(self.__userModel.getUserById(id))

    def triggerUserTableActions(self, id):
        # Check first if current user is allowed to execute the operation/action to be performed.
        if self._auth.get('user_type') == 'Admin' and self._inputs['action'] in ['reactivateUser', 'deactivateUser']:
            return jsonify({
                'result'  : False,
                'title'   : 'Invalid Request',
                'message' : 'You do not have the privileges to perform this action.'
            })

        randomPassword = passHash.generateRandomPassword()
        actionProps = {
            'resetUserPassword' : {
                'queryParams'  : {
                    'set' : {
                        'password': passHash.encrypt(randomPassword)
                    }
                },
                'alertTitle'   : 'Password Reset {}',
                'alertMessage' : '{} new password: "' + randomPassword + '"'
            },
            'reactivateUser'    : {
                'queryParams'  : {
                    'set' : {
                        'status' : 'active'
                    }
                },
                'alertTitle'   : 'Account Reactivation {}',
                'alertMessage' : '{} account has been reactivated.'
            },
            'deactivateUser'    : {
                'queryParams'  : {
                    'set' : {
                        'status' : 'inactive'
                    }
                },
                'alertTitle'   : 'Account Deactivation {}',
                'alertMessage' : '{} account has been deactivated.'
            }
        }
        userDetails = self.__userModel.getUserById(id)
        if userDetails is None:
            result = {
                'result'  : False,
                'title'   : '{} Failed'.format(actionProps[self._inputs['action']]['alertTitle']),
                'message' : 'User not found.'
            }
        else:
            queryParams = actionProps[self._inputs['action']]['queryParams']
            queryParams['where'] = {'id': id}
            self.__userModel.updateUserData(queryParams)
            possessive = '\'s' if userDetails['full_name'][-1] != 's' else '\''
            result = {
                'result'  : True,
                'title'   : actionProps[self._inputs['action']]['alertTitle'].format('Success'),
                'message' : actionProps[self._inputs['action']]['alertMessage'].format(userDetails['full_name'] + possessive)
            }

        return jsonify(result)

    def createUser(self):
        validationResult = self.__validateInputs('createNewUser')
        if validationResult['result'] == False:
            return jsonify(validationResult)

        # Unset the confirm password key.
        self._inputs.pop('confirmPassword', None)

        # Encrypt the password value.
        self._inputs['password'] = passHash.encrypt(self._inputs['password'])

        columnKeys = tuple(self._inputs.keys())
        columnValues = tuple(self._inputs.values())

        # Add the user.
        self.__userModel.addNewUser(columnKeys, columnValues)
        return jsonify({
            'result'  : True,
            'title'   : 'User Creation Success', 
            'message' : 'Account for {} has been successfully created.'.format(self._inputs['full_name'])
        })

    def updateUserDetails(self, id):
        validationResult = self.__validateInputs(self._inputs['action'], id)
        if validationResult['result'] == False:
            return jsonify(validationResult)

        actionToPerform = self._inputs['action']

        # Unset the action key.
        self._inputs.pop('action', None)

        actions = {
            'updateUserDetails' : {
                'queryParams' : {
                    'set'   : self._inputs,
                    'where' : {
                        'id' : id
                    }
                },
                'response'    : {
                    'result'  : True,
                    'title'   : 'User Details Update Success', 
                    'message' : 'Account details for {} has been successfully updated.'.format(self._inputs['full_name'] if 'full_name' in self._inputs else '')
                }
            },
            'updatePassword'    : {
                'queryParams' : {
                    'set'   : {
                        'password' : passHash.encrypt(self._inputs['newPassword']) if 'newPassword' in self._inputs else ''
                    },
                    'where' : {
                        'id' : id
                    }
                },
                'response'    : {
                    'result'  : True,
                    'title'   : 'Password Change Success', 
                    'message' : 'Password for your account has been successfully changed.'
                }
            }
        }
       
        # Update user details.
        self.__userModel.updateUserData(actions[actionToPerform]['queryParams'])

        # Update session details if user details to be updated belongs to the current logged-in user.
        if self._auth.get('id') == int(id):
            userDetails = self.__userModel.getUserBy('id', id)
            self.__updateSession(userDetails)

        return jsonify(actions[actionToPerform]['response'])

    def __validateInputs(self, operation, id = 0):
        # Create an instance of a validator class depending on the operation type.
        operations = {
            'createNewUser'     : CreateNewValidation(),
            'updateUserDetails' : UpdateDetailsValidation(),
            'updatePassword'    : UpdatePasswordValidation()
        }

        validateForm = operations[operation].from_json(self._inputs)

        # Perform validations, and return the validation result to the calling method.
        return validateForm.performValidations(userModel = self.__userModel, userId = id)

    def __updateSession(self, userDetails):
        keysToUnset = ['address', 'contact_num', 'email', 'password', 'status']
        for key in keysToUnset:
            del userDetails[key]

        self._auth.setSession(**userDetails)