from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .users.views import UserViewSet
from .views import IngredientViewSet, RecipeViewSet, TagViewSet


app_name = 'api'
router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns_auth = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

urlpatterns = [
    path('', include(router.urls)),
    path('', include(urlpatterns_auth))
]
