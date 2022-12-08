from recipes.models import Ingredient, Tag
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .serializers import  IngredientSerializer, TagSerializer
from djoser.views import UserViewSet


# class CustomUserViewSet(UserViewSet):
#     serializer_class = CustomUserCreateSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    """Получение ингридиентов."""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class TagViewSet(ReadOnlyModelViewSet):
    """Получение тегов."""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

