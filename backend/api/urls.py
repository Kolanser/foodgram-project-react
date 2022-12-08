from django.urls import include, path
from rest_framework import routers
from .views import IngredientViewSet, TagViewSet

router = routers.DefaultRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredient')
router.register(r'tags', TagViewSet, basename='tag')
urlpatterns = [
    path('', include(router.urls)),
    # path('users/', CustomUserViewSet),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
