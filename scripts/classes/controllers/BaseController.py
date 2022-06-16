from scripts.utilities.sessionHandler import SessionHandler
from flask import request
import json

class BaseController:

    _inputs = {}

    _auth = {}

    def __init__(self):
        self._auth = SessionHandler()
        rawRequestData = request.get_data().decode('utf-8')
        if rawRequestData != '':
            # Convert the raw request data into dictionary.
            self._inputs = json.loads(rawRequestData)
            # Trim whitespaces on all of the inputs.
            for key, value in self._inputs.items():
                if type(value) is str:
                    self._inputs[key] = value.strip()
