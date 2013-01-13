from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns('',
    url('^$', 'website.apwan.views.home.index'),

    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
