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
    except ValueError:
        return None, False
    except TypeError:
        return None, False


def validate_float(value):
    try:
        return float(value), True
    except ValueError:
        return None, False
    except TypeError:
        return None, False


# Base class used for error object classes
class ErrorObject:
    messages = {}
    __path__ = ""


# NOTE: the following error message strings are turned into paths
# and the messages are placed into a 'messages' dictionary
# in each class on import.
class API_ERROR(ErrorObject):
    INVALID_PARAMETER = "Given parameter is invalid"
    NOT_IMPLEMENTED = "Functionality not implemented yet"
    UNKNOWN = "An unknown error occurred"

    class AUTHENTICATION(ErrorObject):
        DEPLOYAUTH_FAILED = "API auth failed or not provided"
        NOT_LOGGED_IN = "You aren't logged in"

    class DONATION(ErrorObject):
        NO_PAYEE = "No Payee available for this recipient"
        SERVICE_FAILED = "Payment platform failed to process our request"

    class ENTITY(ErrorObject):
        NOT_FOUND = "Entity not found"

    class RECIPIENT(ErrorObject):
        ALREADY_CLAIMED = "Recipient has already been claimed"
        LOOKUP_TOKEN_INVALID = "Invalid or expired token supplied"


# Initialize API_ERROR messages
# (Turns error class vars into paths and creates 'messages' dict)
def init_errors(error, parent=None):
    if error == API_ERROR and parent is None:
        error.__path__ = ""

    for attr_key, attr_value in error.__dict__.items():
        if not attr_key.startswith('__') and not attr_key.endswith('__'):
            if type(attr_value) is str or inspect.isclass(attr_value):
                k_path = attr_key
                if error.__path__ != '':
                    k_path = error.__path__ + '.' + k_path

                if inspect.isclass(attr_value):
                    attr_value.__path__ = k_path
                    init_errors(attr_value, error)
                else:
                    if not hasattr(error, 'messages'):
                        error.messages = {}
                    error.messages[attr_key] = error.__dict__[attr_key]
                    error.__dict__[attr_key] = k_path
init_errors(API_ERROR)


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
    name, _, parent = find_error(key)
    if name is None:
        return None
    return parent.messages[name]


def build_error(key, **kwargs):
    name, path, parent = find_error(key)
    if name is None:
        raise ValueError()

    result = {
        'success': False,
        'error': {
            'key': path,
            'message': parent.messages[name]
        }
    }

    for arg_key, arg_value in kwargs.items():
        result['error'][arg_key] = arg_value

    return simplejson.dumps(result)
