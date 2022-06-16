import json

def requestDataToJsonObject(requestData):
    return json.loads(requestData.get_data(as_text = True))

def requestDataToJsonString(requestData):
    return json.dumps(json.loads(requestData.get_data(as_text = True)))