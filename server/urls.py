from django.conf.urls import patterns, include, url
from django.contrib import admin
from server import views
from rest_framework import routers
from server.views import VoteViewSet 

router = routers.DefaultRouter()
router.register(r'votes', VoteViewSet, base_name="vote" )

urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
)
