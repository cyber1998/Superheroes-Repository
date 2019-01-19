import codecs
import csv
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


def get_rows_from_csv(f_path, header=False, delimiter=',',
                      int_fields=[], empty_check_col=None, quoting=False):
    """
     TODO: fix the docstring
    :param f_path:
    f_path - Represents the relative path of the CSV file
    header - Set to True if the first row is to be skipped.
    delimiter - CSV delimiter can be `,`, `;`, etc.
    int_fields - List of columns that has to be converted to integer
        - Empty values are returned as None.
    """

    with codecs.open(f_path, encoding='utf-8', errors='ignore') as f:
        f.seek(0)
        reader = csv.reader(f, delimiter=delimiter)
        if quoting is True:
            reader = csv.reader(f, delimiter=delimiter,  quotechar='"',
                                quoting=csv.QUOTE_ALL, skipinitialspace=True)

        # Skip the header if specified
        if header:
            next(reader)

        rows = []
        for row in reader:
            # Skip row if the required check is empty
            if empty_check_col is not None:
                if row[empty_check_col] == '':
                    continue

            for i, col in enumerate(row):
                row[i] = col.strip()
            rows.append(row)

        return rows


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
