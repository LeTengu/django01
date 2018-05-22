from django.conf.urls import url

from . import views # import views so we can use them in urls.

app_name = 'store'

urlpatterns = [
    url(r'^$', views.listing, name="listing"), # "/store" will call the method "index" in "views.py"
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name="detail"),
    url(r'^search/$', views.search, name="search"),
]