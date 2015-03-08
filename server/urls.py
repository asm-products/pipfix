from django.conf.urls import patterns, include, url
from django.contrib import admin
from server import views
from rest_framework import routers
from server.views import *
from rest_framework_extensions.routers import ExtendedDefaultRouter

router = ExtendedDefaultRouter()

user_router = router.register(r'users', UserViewSet, base_name='user'
    )
user_router.register(r'votes', VoteViewSet, base_name='users-vote',
                parents_query_lookups=['user'])
user_router.register(r'user-stuff', UserStuffViewSet, base_name='users-stuff',
                parents_query_lookups=['user'])
router.register(r'stuff', StuffViewSet, base_name="stuff" 
    ).register(r'votes', VoteViewSet, base_name="stuff-votes",
                parents_query_lookups=['stuff']
    )
router.register(r'timeline', TimelineViewSet, base_name='timeline')


urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
)
