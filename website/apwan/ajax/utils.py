import inspect
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


class API_ERROR:
    INVALID_PARAMETER = "Given parameter is invalid"
    NOT_IMPLEMENTED = "Functionality not implemented yet"
    UNKNOWN = "An unknown error occurred"

    class AUTHENTICATION:
        NOT_LOGGED_IN = "You aren't logged in"

    class DONATION:
        NO_PAYEE = "No Payee available for this recipient"
        SERVICE_FAILED = "Payment platform failed to process our request"

    class ENTITY:
        NOT_FOUND = "Entity not found"

    class RECIPIENT:
        ALREADY_CLAIMED = "Recipient has already been claimed"


# Initialize API_ERROR messages
def init_errors(error=API_ERROR, parent=None):
    if error == API_ERROR and parent is None:
        error.__path__ = ""

    for k, v in error.__dict__.items():
        if not k.startswith('__') and not k.endswith('__'):
            if type(v) is str or inspect.isclass(v):
                k_path = k
                if error.__path__ != '':
                    k_path = error.__path__ + '.' + k_path

                if inspect.isclass(v):
                    v.__path__ = k_path
                    init_errors(v, error)
                else:
                    if not hasattr(error, 'messages'):
                        error.messages = {}
                    error.messages[k] = error.__dict__[k]
                    error.__dict__[k] = k_path
init_errors()


def find_error(key):
    key = key.split('.')
    parent = None
    cur = API_ERROR
    name = None

    for part in key:
        if hasattr(cur, part):
            parent = cur
            cur = getattr(cur, part)
            name = part
        elif hasattr(cur, part.upper()):
            parent = cur
            cur = getattr(cur, part.upper())
            name = part.upper()
        elif hasattr(cur, part.lower()):
            parent = cur
            cur = getattr(cur, part.lower())
            name = part.lower()
        else:
            return None, None, None

    return name, cur, parent


def find_message(key):
    name, path, parent = find_error(key)
    if name is None:
        return None
    return parent.messages[name]


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
