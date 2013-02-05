from django.http import HttpResponse
from django.utils import simplejson

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


class DictObject(object):
    def __init__(self, path="", value=None):
        self.path = path
        self.value = value

    def find(self, key):
        if type(key) is str:
            key = key.split('.')

        if len(key) == 0:
            return self

        cur_key = key.pop(0)
        if hasattr(self, cur_key):
            return getattr(self, cur_key).find(key)
        else:
            return None

    def __str__(self):
        return self.path

    @staticmethod
    def build(dictionary, root=None):
        if root is None:
            root = DictObject()

        for k, v in dictionary.items():
            value = None
            if type(v) is not dict:
                value = v
            item = DictObject((root.path + "." + k).strip('.'), value)
            if type(v) is dict:
                DictObject.build(v, item)
            setattr(root, k, item)

        return root


ERROR = DictObject.build({
    'INVALID_PARAMETER': "Given parameter is invalid",
    'NOT_IMPLEMENTED': "Functionality not implemented yet",
    'UNKNOWN': "Unknown error occurred",

    'AUTHENTICATION': {
        'NOT_LOGGED_IN': "You aren't logged in"
    },

    'DONATION': {
        'NO_PAYEE': "No Payee available for this recipient",
        'SERVICE_FAILED': "Payment platform failed to process our request"
    },

    'ENTITY': {
        'NOT_FOUND': "Entity not found"
    },

    'RECIPIENT': {
        'ALREADY_CLAIMED': "Recipient has already been claimed"
    }
})


def build_error(key, **kwargs):
    error = key
    if type(error) is not DictObject:
        error = ERROR.find(key)

    if error is None:
        error = ERROR.find(key.upper())

    if error is None:
        error = ERROR.find(key.lower())

    if error is None:
        raise KeyError()

    result = {
        'success': False,
        'error': {
            'key': error.path.lower(),
            'message': error.value
        }
    }

    for k, v in kwargs.items():
        result['error'][k] = v

    return simplejson.dumps(result)