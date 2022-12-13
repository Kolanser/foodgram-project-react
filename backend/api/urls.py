from django.urls import include, path
from rest_framework import routers
from .views import (
    IngredientViewSet, RecipeViewSet, TagViewSet, CustomUserViewSet
)


router = routers.DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('tags', TagViewSet, basename='tag')
router.register('recipes', RecipeViewSet, basename='recipe')
router.register('users', CustomUserViewSet, basename='user')
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
