from recipes.models import Ingredient, Recipe, Tag, IngredientRecipe
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer, RecipeWriteSerializer


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
    # serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def perform_create(self, serializer): 
        # title_id = self.kwargs.get('title_id')
        # review_id = self.kwargs.get('review_id')
        # review = get_object_or_404(Review, id=review_id, title__id=title_id)
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'PUT'):
            return RecipeWriteSerializer
        return RecipeSerializer
