from django.conf.urls import url, include
from rest_framework import routers
import viewsets

router  = routers.DefaultRouter()
router.register(r'users', viewsets.UsersViewSet, base_name='customuser')
router.register(r'tasks', viewsets.TasksViewSet, base_name='task')
router.register(r'calls', viewsets.CallsViewSet, base_name='call')
router.register(r'badges', viewsets.BadgesViewSet, base_name='badge')
router.register(r'events', viewsets.EventsViewSet, base_name='event')
router.register(r'categories', viewsets.CategoryViewSet, base_name='category')
router.register(r'userbadges', viewsets.UserBadgesViewSet, base_name='userbadges')
router.register(r'bookmarks', viewsets.BookmarksViewSet, base_name='bookmark')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
