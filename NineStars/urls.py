from django.conf.urls import patterns, include, url

from django.contrib import admin
import OneStar.views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'NineStars.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^dist/(?P<path>.*)', 'django.views.static.serve',{'document_root':'/NineStars/Templates/dist'}),
    url(r'^img/(?P<path>.*)', 'django.views.static.serve',{'document_root':'/NineStars/Templates/images'}),
    url(r'^login/$', 'django.contrib.auth.views.login',{'template_name':'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^$', OneStar.views.index),
    url(r'^test/$', OneStar.views.test),
    url(r'^jqq/$', OneStar.views.jqq),
    url(r'^jqqo/$', OneStar.views.jqqo),
    url(r'^jqqoo/$', OneStar.views.jqqoo),
    url(r'^ref/$', OneStar.views.ref),
    url(r'^refp/$', OneStar.views.refp),
)
