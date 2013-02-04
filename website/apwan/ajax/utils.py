from django.http import HttpResponse

__author__ = 'Dean Gardiner'


def cors_response(data):
    response = HttpResponse(data, mimetype="application/x-json")
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET'
    response['Access-Control-Allow-Headers'] = 'X-PINGOTHER'
    response['Access-Control-Max-Age'] = '1728000'
    return response


def validate_int(value):
    try:
        return int(value), True
    except ValueError, e:
        return None, False
    except TypeError, e:
        return None, False


def validate_float(value):
    try:
        return float(value), True
    except ValueError, e:
        return None, False
    except TypeError, e:
        return None, False