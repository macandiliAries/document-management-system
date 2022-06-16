from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, PasswordField
from wtforms.validators import Length, Email, Regexp, AnyOf, EqualTo
from scripts.utilities.passwordHash import PasswordHash as passHash
from scripts.utilities.sessionHandler import SessionHandler

class UpdatePasswordValidation(FlaskForm):
    oldPassword        = PasswordField(description = 'Invalid Password', validators=[Length(min = 1, message = 'Please enter your old password.')])
    newPassword        = PasswordField(description = 'Invalid Password', validators=[Length(min = 4, message = 'Please enter your new password.')])
    confirmNewPassword = PasswordField(description = 'Invalid Password', validators=[EqualTo('newPassword', message = 'Passwords do not match.')])

    def performValidations(self, **kwargs):
        userId = kwargs['userId']

        if int(userId) == 0:
            return {
                'result'  : False,
                'title'   : 'Invalid Request',
                'message' : 'Invalid user. Please try again.'
            }

        if self.validate() == False:
            # Get the key of the first error encountered.
            errorKey = list(self.errors)[0]
            return {
                'result'  : False,
                'title'   : self[errorKey].description,
                'message' : self.errors[errorKey][0]
            }

        userModel = kwargs['userModel']

        # Check if old password is correct.
        userDetails = userModel.getUserBy('id', userId)
        if passHash.decrypt(userDetails['password']) != self.data['oldPassword']:
            return {
                'result'  : False,
                'title'   : 'Invalid Password',
                'message' : 'Old password is incorrect.'
            }

        return {'result' : True}

class CreateNewValidation(FlaskForm):
    full_name       = StringField(description = 'Invalid Full Name', validators=[Length(min = 4, max = 100, message = 'Full name must be between 4 to 50 characters long.')])
    email           = EmailField(description = 'Invalid Email', validators=[Email(allow_smtputf8 = False)])
    address         = StringField(description = 'Invalid Address', validators=[Length(min = 4, max = 50, message = 'Address must be between 9 to 50 characters long.')])
    contact_num     = TelField(description = 'Invalid Contact Number', validators=[Regexp(regex = '^\d{1,13}$', message = 'Contact number must consist of a maximum of 13 digits.')])
    user_type       = StringField(description = 'Invalid User Role', validators=[AnyOf(values = ['Super Admin', 'Admin'], message = 'Allowed values are: Super Admin, Admin')])
    username        = StringField(description = 'Invalid Username', validators=[
        Length(min = 4, max = 50, message = 'Username must be between 4 to 50 characters long.'),
        Regexp(regex = '^[a-zA-Z\d]+$', message = 'Username must consist of alphanumeric characters only.')
    ])
    password        = StringField(description = 'Invalid Password', validators=[Length(min = 4, message = 'Password must be at least 4 characters long.')])
    confirmPassword = PasswordField(description = 'Invalid Password', validators=[EqualTo('password', message = 'Passwords do not match.')])

    def performValidations(self, **kwargs):
        # Check first if current user is allowed to execute the operation/action to be performed.
        auth = SessionHandler()
        if auth.get('user_type') == 'Admin':
            return {
                'result'  : False,
                'title'   : 'Invalid Request',
                'message' : 'You do not have the privileges to perform this action.'
            }

        if self.validate() == False:
            # Get the key of the first error encountered.
            errorKey = list(self.errors)[0]
            return {
                'result'  : False,
                'title'   : self[errorKey].description,
                'message' : self.errors[errorKey][0]
            }

        userModel = kwargs['userModel']

        # Check if username has been already taken by anyone else.
        userDetails = userModel.getUserBy('username', self.data['username'])
        if userDetails != None:
            return {
                'result'  : False,
                'title'   : 'Invalid Username',
                'message' : 'Username "{}" has already been taken by {}.'.format(userDetails['username'], userDetails['full_name'])
            }

        return {'result' : True}

class UpdateDetailsValidation(FlaskForm):
    full_name       = StringField(description = 'Invalid Full Name', validators=[Length(min = 4, max = 100, message = 'Full name must be between 4 to 50 characters long.')])
    email           = EmailField(description = 'Invalid Email', validators=[Email(allow_smtputf8 = False)])
    address         = StringField(description = 'Invalid Address', validators=[Length(min = 4, max = 50, message = 'Address must be between 9 to 50 characters long.')])
    contact_num     = TelField(description = 'Invalid Contact Number', validators=[Regexp(regex = '^\d{1,13}$', message = 'Contact number must consist of a maximum of 13 digits.')])
    user_type       = StringField(description = 'Invalid User Role', validators=[AnyOf(values = ['Super Admin', 'Admin'], message = 'Allowed values are: Super Admin, Admin')])
    username        = StringField(description = 'Invalid Username', validators=[
        Length(min = 4, max = 50, message = 'Username must be between 4 to 50 characters long.'),
        Regexp(regex = '^[a-zA-Z\d]+$', message = 'Username must consist of alphanumeric characters only.')
    ])

    def performValidations(self, **kwargs):
        # Check first if current user is allowed to execute the operation/action to be performed.
        auth = SessionHandler()
        if auth.get('user_type') == 'Admin':
            if self.data['user_type'] is not None:
                return {
                    'result'  : False,
                    'title'   : 'Invalid Request',
                    'message' : 'You do not have the privileges to perform this action.'
                }

            del self.user_type

        userId = kwargs['userId']
        if int(userId) == 0:
            return {
                'result'  : False,
                'title'   : 'Invalid Request',
                'message' : 'Invalid user. Please try again.'
            }

        if self.validate() == False:
            # Get the key of the first error encountered.
            errorKey = list(self.errors)[0]
            return {
                'result'  : False,
                'title'   : self[errorKey].description,
                'message' : self.errors[errorKey][0]
            }

        userModel = kwargs['userModel']

        # Check if username has been already taken by anyone else.
        userDetails = userModel.getUserByWithIdException('username', self.data['username'], userId)
        if userDetails != None:
            return {
                'result'  : False,
                'title'   : 'Invalid Username',
                'message' : 'Username "{}" has already been taken by {}.'.format(userDetails['username'], userDetails['full_name'])
            }

        return {'result' : True}