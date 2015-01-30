from django.conf.urls import patterns, include, url
from rest_framework import routers
from epm import views
import epm
import ams
from rest_auth import views
from django.conf import settings
from django.conf.urls.static import static

"""
from django.contrib import admin
admin.autodiscover()
"""
import xadmin
xadmin.autodiscover()

# from xadmin.plugins import xversion
# xversion.register_models()


router = routers.DefaultRouter()
# router.register(r'users',views.UserViewSet)
# router.register(r'groups',views.GroupViewSet)
# router.register(r'enterprise',views.EnterpriseViewSet)
# router.register(r'party',views.PartyViewSet)
# router.register(r'member',views.MemberViewSet)
# router.register(r'test',views.TestViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'side.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^xadmin/', include(xadmin.site.urls)),
    url(r'^',include(router.urls)),
    url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework')),
    # url(r'^epm/',include('epm.urls')),
    url(r'^dangjian/laoshanparty/v1/',include('epm.urls')),
    url(r'^dangjian/laoshanparty/v1/',include('ams.urls')),
    url(r'^dangjian/lspmanager/v1/questions',epm.views.worker_question_list),
    url(r'^dangjian/lspmanager/v1/version/',ams.views.get_worker_version),
    url(r'accounts/', include('django.contrib.auth.urls')),
    url(r'accounts/',include('registration.backends.default.urls')),
    # url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^dangjian/laoshanparty/v1/', include('rest_auth.urls')),
    url(r'^dangjian/lspmanager/', include('rest_auth.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
