from flask import jsonify
from scripts.classes.controllers.BaseController import BaseController
from scripts.classes.models.DocumentModel import DocumentModel
from scripts.classes.models.DocumentRevisionModel import DocumentRevisionModel
from scripts.classes.models.DocumentStatusTypeModel import DocumentStatusTypeModel
from scripts.classes.services.DocumentValidation import CreateNewValidation, UpdateExistingValidation, SubmitForReviewValidation, ApprovalValidation, RejectionValidation, TagForRevisionValidation, DeleteValidation
import bleach
import wtforms_json
wtforms_json.init() # Initialize WTForms using JSON values.
from datetime import datetime

class DocumentController(BaseController):

    __docModel = {}

    __docStatusModel = {}

    def __init__(self):
        super().__init__()
        self.__docModel = DocumentModel()
        self.__docRevisionsModel = DocumentRevisionModel()
        self.__docStatusModel = DocumentStatusTypeModel()

    def getDocuments(self):
        documents = self.__docModel.getDocuments()
        for document in documents:
            if document['status'] != 'Approved':
                document['approver'] = '-'
                document['effectiveDate'] = '-'
        return jsonify(documents)

    def getDocumentDetails(self, id):
        return jsonify({
            'documentDetails' : self.__docModel.getDocumentDetails(id),
            'revisionHistory' : self.__docRevisionsModel.getDocumentRevisions(id)
        })
    
    def createDocument(self):
        validationResult = self.__validateInputs('createNewDocument')
        if validationResult['result'] == False:
            return jsonify(validationResult)

        # Prepare other data needed for document creation.
        otherData = {
            'authorId' : self._auth.get('id'),
            'statusId' : 1
        }

        self._inputs.update(otherData)

        columnKeys = tuple(self._inputs.keys())
        columnValues = tuple(self._inputs.values())

        # Insert the document on the table.
        docId = self.__docModel.createNewDocument(columnKeys, columnValues)

        # Insert a record on the revisions table stating that it is the initial creation of the document.
        queryParams = {
            'docId'              : docId,
            'revisionNumber'     : 'v1.0',
            'dateRevised'        : datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
            'significantChanges' : 'Initial creation of the document.',
            'reviserId'          : self._auth.get('id'),
            'isApproved'         : 1
        }

        self.__docRevisionsModel.insertDocumentRevision(tuple(queryParams.keys()), tuple(queryParams.values()))

        return jsonify({
            'result'  : True,
            'title'   : 'Document Creation Success',
            'message' : 'Document has been created and saved as draft.'
        })

    def updateDocument(self, id):
        validationResult = self.__validateInputs('updateDocument', id)
        if validationResult['result'] == False:
            return jsonify(validationResult)

        # Unset the operation key.
        self._inputs.pop('operation', None)

        # Prepare the data needed for document modification.
        otherData = {
            'statusId'     : self.__docStatusModel.getDraftStatus(id)['statusId'],
            'lastEditedBy' : self._auth.get('id'),
            'lastEditedOn' : datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        }

        self._inputs.update(otherData)

        # Prepare the query parameters.
        queryParams = {
            'set'   : self._inputs,
            'where' : {
                'id' : id
            }
        }

        # Update document details.
        self.__docModel.updateExistingDocument(queryParams)

        return jsonify({
            'result'  : True,
            'title'   : 'Document Update Success',
            'message' : 'Document has been updated and saved as draft.'
        })

    def triggerDocsTableActions(self, docId):
        operation = self._inputs['operation']

        # Perform initial validations based on the operation passed from the front-end.
        validationResult = self.__validateInputs(operation, docId)
        if validationResult['result'] == False:
            return jsonify(validationResult)

        # Invoke the (protected) method related to the operation passed using the built-in getattr function.
        return getattr(self, '_' + operation)(docId)

    def _submitDocumentForReview(self, docId):
        # Prepare the query parameters needed for updating the document status.
        queryParams = {
            'set'   : {
                'statusId' : self.__docStatusModel.getSubmissionReviewStatus(docId)['statusId']
            },
            'where' : {
                'id' : docId
            }
        }

        # Update the document status.
        self.__docModel.updateExistingDocument(queryParams)

        # Insert a revision if document to be submitted has been previously tagged as "For Revision".
        if queryParams['set']['statusId'] == 5:
            queryParams = {
                'docId'              : docId,
                'revisionNumber'     : self.__generateNewRevisionVersion(self.__docRevisionsModel.getDocumentRevisions(docId)),
                'dateRevised'        : datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                'significantChanges' : bleach.clean(self._inputs['significantChanges']),
                'reviserId'          : self.__docModel.getDocumentDetails(docId)['lastEditorId']
            }

            # Insert revision history.
            self.__docRevisionsModel.insertDocumentRevision(tuple(queryParams.keys()), tuple(queryParams.values()))

        return jsonify({
            'result'  : True,
            'title'   : 'Document Submission Success',
            'message' : 'Document is now subject for review.'
        })

    def _approveDocument(self, docId):
        # Approve the revision if document to be approved has been previously tagged as "For Revision Review".
        if self.__docModel.getDocumentDetails(docId)['status'] == 'For Revision Review':
            queryParams = {
                'set'   : {
                    'isApproved' : 1
                },
                'where' : {
                    'id' : self.__docRevisionsModel.getDocumentRevisions(docId)[0]['revisionId'] # Approve the latest revision history associated with the document.
                }
            }
            self.__docRevisionsModel.updateDocumentRevision(queryParams)

        # Prepare the query parameters needed for approving the document.
        queryParams = {
            'set'   : {
                'statusId'      : 3, # Approved
                'effectiveDate' : datetime.today().strftime('%Y-%m-%d %H:%M:%S'), # Current Timestamp
                'approverId'    : self._auth.get('id')
            },
            'where' : {
                'id' : docId
            }
        }

        # Update the document status.
        self.__docModel.updateExistingDocument(queryParams)

        return jsonify({
            'result'  : True,
            'title'   : 'Document Approval Success',
            'message' : 'Document is now tagged as Approved.'
        })

    def _denyDocument(self, docId):
        # Delete the supposed revision changes if document to be denied has been previously tagged as "For Revision Review".
        if self.__docModel.getDocumentDetails(docId)['status'] == 'For Revision Review':
            lastRevisionId = self.__docRevisionsModel.getDocumentRevisions(docId)[0]['revisionId']
            self.__docRevisionsModel.deleteDocumentRevision(lastRevisionId)
  
        # Prepare the query parameters needed for updating the document status back to drafts.
        queryParams = {
            'set'   : {
                'statusId' : self.__docStatusModel.getRejectStatus(docId)['statusId']
            },
            'where' : {
                'id' : docId
            }
        }

        # Update the document status.
        self.__docModel.updateExistingDocument(queryParams)

        return jsonify({
            'result'  : True,
            'title'   : 'Document Rejection Success',
            'message' : 'Document has been denied and back to Drafts.'
        })

    def _tagDocumentForRevision(self, docId):
        # Prepare the query parameters needed for updating the document status back to drafts.
        queryParams = {
            'set'   : {
                'statusId' : 4 # For Revision
            },
            'where' : {
                'id' : docId
            }
        }

        # Update the document status.
        self.__docModel.updateExistingDocument(queryParams)

        return jsonify({
            'result'  : True,
            'title'   : 'Revision Tagging Success',
            'message' : 'Document has been tagged as for revision.'
        })

    def _deleteDocument(self, docId):
        # Delete the document, together with the associated revisions for it (via ON DELETE CASCADE).
        self.__docModel.deleteDocument(docId)

        return jsonify({
            'result'  : True,
            'title'   : 'Document Deletion Success',
            'message' : 'Document has been permanently deleted.'
        })

    def __validateInputs(self, operation, docId = 0):
        # Create an instance of a validator class depending on the operation type.
        operations = {
            'createNewDocument'       : CreateNewValidation(),
            'updateDocument'          : UpdateExistingValidation(),
            'submitDocumentForReview' : SubmitForReviewValidation(),
            'approveDocument'         : ApprovalValidation(),
            'denyDocument'            : RejectionValidation(),
            'tagDocumentForRevision'  : TagForRevisionValidation(),
            'deleteDocument'          : DeleteValidation()
        }

        # Initialize the fields to be validated.
        validateForm = operations[operation].from_json(self._inputs)

        # Perform validations, and return the validation result to the calling method.
        return validateForm.performValidations(docId = docId, docModel = self.__docModel)

    def __generateNewRevisionVersion(self, revisionHistory):
        # Get the latest revision, and evaluate the value.
        lastRevisionMajorVersion = int(revisionHistory[0]['revisionNumber'].split('.')[0][1:])
        lastRevisionMinorVersion = int(revisionHistory[0]['revisionNumber'].split('.')[1])
        
        if lastRevisionMinorVersion < 9:
            lastRevisionMinorVersion += 1
        else:
            lastRevisionMajorVersion += 1
            lastRevisionMinorVersion = 0 

        return "v{}.{}".format(lastRevisionMajorVersion, lastRevisionMinorVersion)