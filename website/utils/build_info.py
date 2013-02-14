import os
from django.utils import simplejson

__author__ = 'Dean Gardiner'


def load(path):
    if os.path.exists(path):
        _file = open(path)
        _json = simplejson.load(_file)
        _file.close()

        BUILD_ID = _json.get('BUILD_ID')
        BUILD_NUMBER = _json.get('BUILD_NUMBER')
        GIT_BRANCH = _json.get('GIT_BRANCH')
        GIT_COMMIT = _json.get('GIT_COMMIT')

        GIT_COMMIT_SHORT = GIT_COMMIT
        if GIT_COMMIT and len(GIT_COMMIT_SHORT) > 7:
            GIT_COMMIT_SHORT = GIT_COMMIT_SHORT[:7]

        UPSTREAM_BUILD_NUMBER = _json.get('UPSTREAM_BUILD_NUMBER')
        if UPSTREAM_BUILD_NUMBER == '':
            UPSTREAM_BUILD_NUMBER = None

        UPSTREAM_JOB_NAME = _json.get('UPSTREAM_JOB_NAME')
        if UPSTREAM_JOB_NAME == '':
            UPSTREAM_JOB_NAME = None

        if (BUILD_ID or BUILD_NUMBER or
                GIT_BRANCH or GIT_COMMIT or
                UPSTREAM_BUILD_NUMBER or UPSTREAM_JOB_NAME):
            BUILD_INFO_EXISTS = True

        return {
            'BUILD_ID': BUILD_ID,
            'BUILD_NUMBER': BUILD_NUMBER,

            'GIT_BRANCH': GIT_BRANCH,
            'GIT_COMMIT': GIT_COMMIT,
            'GIT_COMMIT_SHORT': GIT_COMMIT_SHORT,

            'UPSTREAM_BUILD_NUMBER': UPSTREAM_BUILD_NUMBER,
            'UPSTREAM_JOB_NAME': UPSTREAM_JOB_NAME
        }
    return {}


def to_html(build_info):
    _html_elements = []

    BUILD_ID = build_info.get('BUILD_ID')
    BUILD_NUMBER = build_info.get('BUILD_NUMBER')
    GIT_BRANCH = build_info.get('GIT_BRANCH')
    GIT_COMMIT = build_info.get('GIT_COMMIT')
    GIT_COMMIT_SHORT = build_info.get('GIT_COMMIT_SHORT')
    UPSTREAM_BUILD_NUMBER = build_info.get('UPSTREAM_BUILD_NUMBER')
    UPSTREAM_JOB_NAME = build_info.get('UPSTREAM_JOB_NAME')

    # BUILD_NUMBER
    if BUILD_NUMBER:
        _html_elements.append("<a href=\"%s\">deploy-%s</a>" % (
            "http://buildbot.skipthe.net/job/Fruct.us%%20Website%%20-%%20Deploy/%s/" % (
                BUILD_NUMBER
            ),
            BUILD_NUMBER
        ))

    # UPSTREAM_*
    if UPSTREAM_BUILD_NUMBER and UPSTREAM_JOB_NAME:
        _html_elements.append("<a href=\"%s\">build-%s</a>" % (
            "http://buildbot.skipthe.net/job/%s/%s" % (
                UPSTREAM_JOB_NAME, UPSTREAM_BUILD_NUMBER
            ),
            UPSTREAM_BUILD_NUMBER
        ))

    # GIT_*
    if GIT_BRANCH and GIT_COMMIT:
        _html_elements.append("<a href=\"%s\">%s</a>" % (
            "https://github.com/FructusCode/website/commit/%s/%s" % (
                GIT_BRANCH, GIT_COMMIT
            ),
            "%s/%s" % (GIT_BRANCH, GIT_COMMIT_SHORT)
        ))
    elif GIT_BRANCH:
        _html_elements.append("<a href=\"%s\">%s</a>" % (
            "https://github.com/FructusCode/website/commits/%s" % GIT_BRANCH,
            GIT_BRANCH
        ))
    elif GIT_COMMIT:
        _html_elements.append("<a href=\"%s\">%s</a>" % (
            "https://github.com/FructusCode/website/commit/%s" % GIT_COMMIT,
            "%s" % GIT_COMMIT_SHORT
        ))

    # BUILD_ID
    if BUILD_ID:
        _html_elements.append(BUILD_ID)

    # Join all the html elements
    return " - ".join(_html_elements)
