from recipes.models import Ingredient, Recipe, Tag
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .serializers import  IngredientSerializer, RecipeSerializer, TagSerializer
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


class RecipeViewSet(ModelViewSet):
    """Получение рецептов."""
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()