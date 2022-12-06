from recipes.models import Ingredient, Tag
from rest_framework import  serializers


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели Ingredient."""

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели Tag."""

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag
