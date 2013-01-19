from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns('',
    url('^$', 'django.views.generic.simple.redirect_to', {'url': '/home'}),
    url('^home/$', 'website.apwan.views.home.index'),

    # Account
    url('^account/$', 'django.views.generic.simple.redirect_to', {'url': '/account/profile'}),
    url('^account/profile/$', 'website.apwan.views.account.index'),
    url('^account/login/$', 'django.contrib.auth.views.login', {'template_name': 'account/login.html'}),
    url('^account/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/home'}),

    url('^account/payee/add/$', 'website.apwan.views.account.payee_add'),
    url(r'^account/payee/(?P<slug>.*)/edit/$', 'website.apwan.views.account.payee_edit'),
    url(r'^account/payee/(?P<slug>.*)/$', 'website.apwan.views.account.payee_view'),
    url('^account/payee/add/wepay/$', 'website.apwan.views.account.payee_add_wepay'),

    url('^account/recipient/claim/$', 'website.apwan.views.account.recipient_claim'),

    url('^account/report/donations/$', 'website.apwan.views.account.report_donations'),

    # Dev
    url('^dev/$', 'website.apwan.views.dev.index'),
    url('^dev/entity/search/$', 'website.apwan.views.dev.entity_search'),
    url('^dev/donation/checkout/$', 'website.apwan.views.dev.donation_checkout'),
    url('^dev/wepay/account/find/$', 'website.apwan.views.dev.wepay_account_find'),
    url('^dev/wepay/checkout/create/$', 'website.apwan.views.dev.wepay_checkout_create'),

    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
