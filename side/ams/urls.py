from django.conf.urls import patterns,url,include
from ams import views
urlpatterns = patterns('',
    url(r'^comment/$',views.submit_comment),
    url(r'^version/$',views.get_version),
)
