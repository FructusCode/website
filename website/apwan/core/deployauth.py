import hashlib
from website import settings
from website.apwan.core.api_utils import build_error, API_ERROR

__author__ = 'Dean Gardiner'


def deployauth_required(function):
    def wrapper(request, *args, **kwargs):
        if settings.FRUCTUS_DEPLOYMENT == 'OPEN':
            return function(*args, **kwargs)
        else:
            # Cookie auth (API is used on the website)
            if request.user.is_authenticated() and request.user.is_active:
                if settings.FRUCTUS_DEPLOYMENT == 'INTERNAL' and request.user.is_staff:
                    return function(*args, request=request, **kwargs)
                elif settings.FRUCTUS_DEPLOYMENT == 'INVITE':
                    return function(*args, request=request, **kwargs)

            # deployauth token (API is used remotely)
            if 'deployauth_token' in kwargs:
                if deployauth_token_validate(kwargs['deployauth_token']):
                    return function(*args, **kwargs)

        return build_error(API_ERROR.AUTHENTICATION.DEPLOYAUTH_FAILED)
    return wrapper


def deployauth_token_validate(token):
    from website.apwan.models.user_profile import UserProfile
    profiles = UserProfile.objects.filter(deployauth_token=token)
    if len(profiles) == 1 and profiles[0].deployauth_token == token:
        return True
    return False


def deployauth_token_update(profile):
    md5_hash = hashlib.md5()
    # pylint: disable=E1101
    md5_hash.update(profile.user.username)
    md5_hash.update(profile.user.password)
    profile.deployauth_token = md5_hash.hexdigest()
    # pylint: enable=E1101
