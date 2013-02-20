from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'django.views.generic.simple.redirect_to', {'url': '/home'}),
    url(r'^home/$', 'website.apwan.views.home.index'),

    # /account
    url(r'^account/$', 'django.views.generic.simple.redirect_to', {'url': '/account/profile'},
        name='account'),
    url(r'^account/profile/$', 'website.apwan.views.account.index',
        name='account-profile'),
    url(r'^account/login/$', 'django.contrib.auth.views.login', {'template_name': 'account/login.html'}),
    url(r'^account/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/home'}),

    # /account/(payee, add_payee)
    url(r'^account/add_payee/$', 'website.apwan.views.account.payee_add',
        name='account-payee-add'),

    url(r'^account/add_payee/braintree/$', 'website.apwan.views.account.payee_add_form',
        {'platform_key': 'braintree'}, name='account-payee-add-braintree'),
    url(r'^account/add_payee/wepay/$', 'website.apwan.views.account.payee_add_wepay',
        name='account-payee-add-wepay'),

    url(r'^account/payee/(?P<slug>.*)/settings/$','website.apwan.views.account.payee_settings',
        name='account-payee-edit'),
    url(r'^account/payee/(?P<slug>.*)/$','website.apwan.views.account.payee_view',
        name='account-payee-view'),

    # /account/(recipient, claim_recipient)
    url('^account/claim_recipient/$','website.apwan.views.account.recipient_claim',
        name='account-recipient-claim'),
    url(r'^account/recipient/(?P<slug>.*)/settings/$','website.apwan.views.account.recipient_settings',
        name='account-recipient-edit'),
    url(r'^account/recipient/(?P<slug>.*)/$','website.apwan.views.account.recipient_view',
        name='account-recipient-view'),

    # /account/report
    url(r'^account/report/donations/$', 'website.apwan.views.account.report_donations',
        name='account-report-donations'),

    # /donation
    url(r'^donation/checkout/(?P<donation_id>\d+)/$',
        'website.apwan.views.donation.checkout', name='donation-checkout'),
    url(r'^donation/confirm/(?P<donation_id>\d+)/$',
        'website.apwan.views.donation.confirm', name='donation-confirm'),
    url(r'^donation/complete/(?P<donation_id>\d+)/$',
        'website.apwan.views.donation.complete', name='donation-complete'),

    # /callback
    url(r'^callback/wepay/checkout/$', 'website.apwan.views.callback.wepay_checkout',
        name='callback-wepay-checkout'),

    # Dev
    url(r'^dev/$', 'website.apwan.views.dev.index'),
    url(r'^dev/entity/search/$', 'website.apwan.views.dev.entity_search'),
    url(r'^dev/donation/create/$', 'website.apwan.views.dev.donation_create'),
    url(r'^dev/wepay/account/find/$', 'website.apwan.views.dev.wepay_account_find'),
    url(r'^dev/wepay/checkout/create/$', 'website.apwan.views.dev.wepay_checkout_create'),

    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
