from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .users.views import UserViewSet


app_name = 'api'
router = DefaultRouter()

router.register('users', UserViewSet, basename='users')

urlpatterns_auth = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

urlpatterns = [
    path('', include(router.urls)),
    path('', include(urlpatterns_auth))
]
