from django.conf.urls import patterns, url

from auction import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<category_name>\w+)$', views.auctions_list, name='auctions_list'),
    url(r'^(?P<category_name>\w+)/(?P<auction_id>\d+)$', views.details, name='details'),
    url(r'^bid/$', views.bid, name='bid'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^favorites/$', views.favorites, name='favorites'),
)
