from django.conf.urls import url

from . import views
app_name = 'inventory'
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    #url(r'^(?P<book_id>[0-9]+)/$', views.detail, name='detail'),
    #url(r'^search/$', views.search, name='search'),
    #url(r'^add/(?P<searchTerm>\w*)$', views.add, name = 'add'),
]