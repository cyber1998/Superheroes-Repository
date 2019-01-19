import json
from flask import (
    Flask,
    Response
)


def respond(data, message=None, http_status=200,  pagination=None):
    """
    Argument data refers to data or errors, the latter in case of the
    http_status being 4xx or 5xx.
    status:         str - 'success'/'error'
    http_status:    int - 200 to 599
    data (success): array/dictionary/None - contains the data
    data (error):   array -
    """

    if pagination:
        if http_status < 400:
            return {
                'response_type': 'success',
                'http_status': http_status,
                'data': data,
                'pagination': pagination,
                'description': message
            }
        else:
            return {
                'response_type': 'error',
                'http_status': http_status,
                'errors': data,
                'pagination': pagination,
                'description': message
            }
    else:

        if http_status < 400:
            return {
                'response_type': 'success',
                'http_status': http_status,
                'data': data,
                'description': message
            }
        else:
            return {
                'response_type': 'error',
                'http_status': http_status,
                'errors': data,
                'description': message
            }


class ApiFlask(Flask):
    """
    Inherited from the Flask class to override the make_response
    function to automatically convert a returned dictionary to a JSON
    response.
    """

    def make_response(self, rv):
        if isinstance(rv, dict):
            return Response(
                json.dumps(rv, sort_keys=False),
                status=rv['http_status'],
                mimetype='application/json',
            )
        return Flask.make_response(self, rv)
