from djoser.serializers import UserSerializer
from recipes.models import CustomUser, Ingredient, Tag
from rest_framework import serializers


class CustomUserSerializer(UserSerializer):
    class Meta:
        # model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


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
