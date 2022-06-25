from flask import current_app as app, jsonify
from flask_mail import Mail, Message

class Mailer:

    __template = ''

    __templates = {
        'For Review'          : {
            'title'      : 'Document Management System - Document For Review',
            'recipients' : ['testEmailRecipient@test.com'],
            'message'    : '<h2>Document For Review</h2><p>{executor_name} has submitted the "{document_title}" document for review.</p>'
        },
        'Approved'            : {
            'title'      : 'Document Management System - Document Approved',
            'recipients' : ['testEmailRecipient@test.com'],
            'message'    : '<h2>Document Approved</h2><p>The "{document_title}" document submitted by {executor_name} has been approved.</p>'
        },
        'Denied'              : {
            'title'      : 'Document Management System - Document Denied',
            'recipients' : ['testEmailRecipient@test.com'],
            'message'    : '<h2>Document Denied</h2><p>The "{document_title}" document submitted by {executor_name} has been denied.</p>'
        },
        'For Revision'        : {
            'title'      : 'Document Management System - For Revision',
            'recipients' : ['testEmailRecipient@test.com'],
            'message'    : '<h2>Document Tagged for Revision</h2><p>The "{document_title}" document has been tagged for revision by {executor_name}.</p>'
        },
        'For Revision Review' : {
            'title'      : 'Document Management System - Document For Revision Review',
            'recipients' : ['testEmailRecipient@test.com'],
            'message'    : '<h2>Document Revision For Review</h2><p>{executor_name} has submitted the "{document_title}" document for revision review.</p>'
        }
    }

    __mailer = {}

    __message = {}

    __params = []

    def __init__(self):
        self.__mailer = Mail(app)

    def setTemplate(self, template):
        self.__template = template

    def setParams(self, params):
        self.__params = params

    def sendMail(self):
        try:
            self.__message = Message(self.__templates[self.__template]['title'])
            self.__message.html = self.__templates[self.__template]['message'].format(**self.__params)
            self.__message.recipients = self.__templates[self.__template]['recipients']
            self.__mailer.send(self.__message)
            result = {'result': True}
        except Exception as e:
            print(e)
            result = {'result': False, 'message': str(e)}

        return jsonify(result)