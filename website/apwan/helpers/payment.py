from wepay import WePay
from website.keys import WEPAY_PRODUCTION, WEPAY_ACCESS_TOKEN

__author__ = 'Dean Gardiner'

wepay = WePay(production=WEPAY_PRODUCTION, access_token=WEPAY_ACCESS_TOKEN)


def get_authorization():
    pass