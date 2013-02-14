from django.conf import settings

__author__ = 'Dean Gardiner'


def template_settings(request):
    """Add variables from the django settings file to template contexts.

    Adds settings from the GLOBAL_SETTINGS_KEYS list (in django.conf.settings)
    to the every template context.
    """
    settings_dict = {}

    if hasattr(settings, 'TEMPLATE_SETTINGS'):
        for key in settings.TEMPLATE_SETTINGS:
            if hasattr(settings, key):
                settings_dict[key] = getattr(settings, key)

    return {'settings': settings_dict}
