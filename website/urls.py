from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns('',
    url('^$', 'django.views.generic.simple.redirect_to', {'url': '/home'}),
    url('^home/$', 'website.apwan.views.home.index'),

    # Account
    url('^account/$', 'website.apwan.views.account.index'),
    url('^account/login/$', 'django.contrib.auth.views.login', {
        'template_name': 'account/login.html'
    }),
    url('^account/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/home'}),

    # Dev
    url('^dev/$', 'website.apwan.views.dev.index'),
    url('^dev/search/$', 'website.apwan.views.dev.search'),

    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
