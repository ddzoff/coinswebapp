from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'coinswebapp.views.index', name='index'),
    url(r'^home/', 'coinswebapp.views.home', name='home'),
    url(r'^auction/', include('auction.urls')),
    url(r'^register/$', 'coinswebapp.views.register', name='register'),
    url(r'^login/$', 'coinswebapp.views.user_login', name='login'),
    url(r'^logout/$', 'coinswebapp.views.user_logout', name='logout'),

    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
