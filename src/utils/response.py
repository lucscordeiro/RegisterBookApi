import json
from flask import Response


def response(status, name_of_content, content, message=""):
    body = {}
    body[name_of_content] = content
    if message:
        body['message'] = message
    return Response(json.dumps(body), status=status, mimetype="application/json")
