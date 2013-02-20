import re
from django.template.defaultfilters import slugify

__author__ = 'Dean Gardiner'

#
# unique_slugify + _slug_strip
#
# http://djangosnippets.org/snippets/690/
# http://djangosnippets.org/users/SmileyChris/
#


def unique_slugify(instance, value, slug_field_name='slug', queryset=None,
                   slug_separator='-'):
    """
    Calculates and stores a unique slug of ``value`` for an instance.

    ``slug_field_name`` should be a string matching the name of the field to
    store the slug in (and the field to check against for uniqueness).

    ``queryset`` usually doesn't need to be explicitly provided - it'll default
    to using the ``.all()`` queryset from the model's default manager.
    """
    slug_field = instance._meta.get_field(slug_field_name)

    slug = getattr(instance, slug_field.attname)
    slug_len = slug_field.max_length

    # Sort out the initial slug, limiting its length if necessary.
    slug = slugify(value)
    if slug_len:
        slug = slug[:slug_len]
    slug = _slug_strip(slug, slug_separator)
    original_slug = slug

    # Create the queryset if one wasn't explicitly provided and exclude the
    # current instance from the queryset.
    if queryset is None:
        queryset = instance.__class__._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    # Find a unique slug. If one matches, at '-2' to the end and try again
    # (then '-3', etc).
    _next = 2
    while not slug or queryset.filter(**{slug_field_name: slug}):
        slug = original_slug
        end = '%s%s' % (slug_separator, _next)
        if slug_len and len(slug) + len(end) > slug_len:
            slug = slug[:slug_len - len(end)]
            slug = _slug_strip(slug, slug_separator)
        slug = '%s%s' % (slug, end)
        _next += 1

    setattr(instance, slug_field.attname, slug)


def _slug_strip(value, separator='-'):
    """
    Cleans up a slug by removing slug separator characters that occur at the
    beginning or end of a slug.

    If an alternate separator is used, it will also replace any instances of
    the default '-' separator with the new separator.
    """
    separator = separator or ''
    if separator == '-' or not separator:
        re_sep = '-'
    else:
        re_sep = '(?:-|%s)' % re.escape(separator)
        # Remove multiple instances and if an alternate separator is provided,
    # replace the default '-' separator.
    if separator != re_sep:
        value = re.sub('%s+' % re_sep, separator, value)
        # Remove separator from the beginning and end of the slug.
    if separator:
        if separator != '-':
            re_sep = re.escape(separator)
        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
    return value

#
# sql_auto_increment
#
# http://djangosnippets.org/snippets/1415/
# http://djangosnippets.org/users/bernie2004/
#
# Added SQLite support ~ fuzeman
#


def sql_auto_increment(model):
    from django.db import connection
    cursor = connection.cursor()

    # This is ugly, deal with it.
    # We are unable to do an actual type check..
    cursor_name = str(type(cursor.cursor))

    if cursor_name == "<class 'django.db.backends.sqlite3.base.SQLiteCursorWrapper'>":
        cursor.execute("SELECT MAX(id) AS max_id FROM %s" % model._meta.db_table)
        row = cursor.fetchone()
        cursor.close()

        if len(row) != 1:
            raise IndexError()
        if row[0] is None:
            return 1
        return row[0] + 1

    elif cursor_name == "<class 'django.db.backends.mysql.base.CursorWrapper'>":
        cursor.execute("SELECT Auto_increment FROM information_schema.tables "
                       "WHERE table_name='%s';" % model._meta.db_table)
        row = cursor.fetchone()
        cursor.close()

        if len(row) != 1:
            raise ValueError()
        return row[0]

    else:
        raise NotImplementedError()
