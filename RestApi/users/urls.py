from django.urls import path, include

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

from .views import UserViewSet, ClientViewSet, ProjectViewSet

user_router = routers.DefaultRouter()

user_router.register(r'users', UserViewSet, 'User')
user_router.register(r'client', ClientViewSet, 'client')
user_router.register(r'project', ProjectViewSet, 'project')

urlpatterns = [
    path('', include(user_router.urls)),

]
urlpatterns = format_suffix_patterns(urlpatterns)
