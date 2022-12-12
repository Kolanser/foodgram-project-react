from django.urls import include, path
from rest_framework import routers
from .views import (
    FollowViewSet, IngredientViewSet, RecipeViewSet, TagViewSet
)


router = routers.DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('tags', TagViewSet, basename='tag')
router.register('recipes', RecipeViewSet, basename='recipe')
router.register('users', FollowViewSet, basename='subscription')
# router.register(
#     'users',
#     FollowViewSet,
#     basename='set_subscription'
# )
urlpatterns = [
    path('', include('djoser.urls')),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
