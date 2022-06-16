from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length, Email, AnyOf, NoneOf
from scripts.classes.models.DocumentTypeModel import DocumentTypeModel
from scripts.utilities.sessionHandler import SessionHandler

def getDocumentTypeIds():
    documentTypes = DocumentTypeModel().getDocumentTypes()
    docTypeIds = [str(data['id']) for data in documentTypes]
    return docTypeIds

def isSuperAdmin():
    return SessionHandler().get('user_type') == 'Super Admin'

def isExistingDocumentTitle(documents, documentTitle, docId = 0):
    for document in documents:
        if document['title'] == documentTitle:
            returnValue = True
            if document['docId'] == int(docId):
                returnValue = False

            return returnValue

    return False

invalidReturnReponse = {
    'result'  : False,
    'title'   : 'Invalid Request',
    'message' : 'Invalid document. Please try again.'
}

invalidPrivilegeResponse = {
    'result'  : False,
    'title'   : 'Invalid Request',
    'message' : 'You do not have the privileges to perform this action.'
}

class CreateNewValidation(FlaskForm):
    title     = StringField(description = 'Invalid Title', validators=[Length(min = 3, message = 'Please enter at least 3 characters for the document title.')])
    docTypeId = StringField(description = 'Invalid Document Type', validators=[AnyOf(values = getDocumentTypeIds(), message = 'Please select a valid document type.')])
    contents  = StringField(description = 'Invalid Document Contents', validators=[NoneOf(values = ['<p><br></p>'], message = 'Please enter some content for the document.'), ])

    def performValidations(self, **kwargs):
        if self.validate() == False:
            # Get the key of the first error encountered.
            errorKey = list(self.errors)[0]
            return {
                'result'  : False,
                'title'   : self[errorKey].description,
                'message' : self.errors[errorKey][0]
            }

        documents = kwargs['docModel'].getDocuments()
        if isExistingDocumentTitle(documents, self.data['title']) == True:
            return {
                'result'  : False,
                'title'   : 'Invalid Title',
                'message' : 'Document title already taken.'
            }

        return {'result' : True}

class UpdateExistingValidation(FlaskForm):
    title     = StringField(description = 'Invalid Title', validators=[Length(min = 3, message = 'Please enter at least 3 characters for the document title.')])
    docTypeId = StringField(description = 'Invalid Document Type', validators=[AnyOf(values = getDocumentTypeIds(), message = 'Please select a valid document type.')])
    contents  = StringField(description = 'Invalid Document Contents', validators=[NoneOf(values = ['<p><br></p>'], message = 'Please enter some content for the document.'), ])

    def performValidations(self, **kwargs):
        docId = kwargs['docId']

        if int(docId) == 0:
            return invalidReturnReponse

        if self.validate() == False:
            # Get the key of the first error encountered.
            errorKey = list(self.errors)[0]
            return {
                'result'  : False,
                'title'   : self[errorKey].description,
                'message' : self.errors[errorKey][0]
            }

        documents = kwargs['docModel'].getDocuments()
        if isExistingDocumentTitle(documents, self.data['title'], docId) == True:
            return {
                'result'  : False,
                'title'   : 'Invalid Title',
                'message' : 'Document title already taken.'
            }

        return {'result' : True}

class SubmitForReviewValidation(FlaskForm):
    significantChanges = StringField(description = 'Invalid Changes', validators=[Length(min = 1, message = 'Revision details should not be left blank.')])

    def performValidations(self, **kwargs):
        docId = kwargs['docId']

        if int(docId) == 0:
            return invalidReturnReponse

        # Check the document's status if eligible for review.
        docDetails = kwargs['docModel'].getDocumentDetails(docId)
        if docDetails['status'] not in ['Draft', 'Draft Revision']:
            return {
                'result'  : False,
                'title'   : 'Invalid Request',
                'message' : 'Document cannot be submitted for review.'
            }

        if docDetails['status'] == 'Draft Revision' and self.validate() == False:
            # Get the key of the first error encountered.
            errorKey = list(self.errors)[0]
            return {
                'result'  : False,
                'title'   : self[errorKey].description,
                'message' : self.errors[errorKey][0]
            }

        return {'result' : True}

class ApprovalValidation(FlaskForm):

    def performValidations(self, **kwargs):
        if isSuperAdmin() == False:
            return invalidPrivilegeResponse

        docId = kwargs['docId']

        if int(docId) == 0:
            return invalidReturnReponse

        # Check the document's status if eligible to be approved.
        docDetails = kwargs['docModel'].getDocumentDetails(docId)
        if docDetails['status'] not in ['For Review', 'For Revision Review']:
            return {
                'result'  : False,
                'title'   : 'Invalid Request',
                'message' : 'Document cannot be approved.'
            }

        return {'result' : True}

class RejectionValidation(FlaskForm):

    def performValidations(self, **kwargs):
        if isSuperAdmin() == False:
            return invalidPrivilegeResponse

        docId = kwargs['docId']

        if int(docId) == 0:
            return invalidReturnReponse

        # Check the document's status if eligible to be rejected.
        docDetails = kwargs['docModel'].getDocumentDetails(docId)
        if docDetails['status'] not in ['For Review', 'For Revision Review']:
            return {
                'result'  : False,
                'title'   : 'Invalid Request',
                'message' : 'Document cannot be rejected.'
            }

        return {'result' : True}

class TagForRevisionValidation(FlaskForm):

    def performValidations(self, **kwargs):
        if isSuperAdmin() == False:
            return invalidPrivilegeResponse

        docId = kwargs['docId']

        if int(docId) == 0:
            return invalidReturnReponse

        # Check the document's status if eligible to be tagged for revision.
        docDetails = kwargs['docModel'].getDocumentDetails(docId)
        if docDetails['status'] not in ['Approved']:
            return {
                'result'  : False,
                'title'   : 'Invalid Request',
                'message' : 'Document cannot be tagged for revision.'
            }

        return {'result' : True}

class DeleteValidation(FlaskForm):

    def performValidations(self, **kwargs):
        if isSuperAdmin() == False:
            return invalidPrivilegeResponse

        docId = kwargs['docId']

        if int(docId) == 0:
            return invalidReturnReponse

        return {'result' : True}