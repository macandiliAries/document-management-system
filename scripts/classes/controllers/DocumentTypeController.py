from scripts.classes.controllers.BaseController import BaseController
from scripts.classes.models.DocumentTypeModel import DocumentTypeModel
from flask import jsonify

class DocumentTypeController(BaseController):

    __docTypeModel = {}

    def __init__(self):
        super().__init__()
        self.__docTypeModel = DocumentTypeModel()

    def getDocumentTypes(self):
        return jsonify(self.__docTypeModel.getDocumentTypes())