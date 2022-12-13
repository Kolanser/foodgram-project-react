from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from djoser.conf import settings
from recipes.models import (
    CustomUser, Follow, Ingredient, IngredientRecipe, Recipe, Tag
)
from rest_framework import serializers


class CustomUserSerializer(UserSerializer):
    """Сериализатор для пользователя."""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = tuple(CustomUser.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
        ) + ('is_subscribed', )
        read_only_fields = (settings.LOGIN_FIELD, 'is_subscribed')

    def get_is_subscribed(self, obj):
        return self.context['request'].user.subscriptions.filter(
            following_id=obj.id
            ).exists()


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели Ingredient."""

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient
        read_only_fields = ('name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели Tag."""

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag
        read_only_fields = ('name', 'color', 'slug')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели IngredientRecipe."""
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    id = serializers.ReadOnlyField(source='ingredient.id')

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = IngredientRecipe


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели рецептов."""
    tags = TagSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(
        source='ingredientrecipe_set', many=True
    )

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        model = Recipe
        read_only_fields = ('id',)

    # def create(self, validated_data):
    #         validated_data.pop('tags')
    #         validated_data.pop('ingredientrecipe_set')
    #         recipe = Recipe.objects.create(**validated_data)
    #         tags = self.initial_data.get('tags')
    #         ingredients = self.initial_data.get('ingredients')
    #         for ingredient in ingredients:
    #             current_ingredient = get_object_or_404(
    #                 Ingredient,
    #                 id=ingredient.get('id')
    #             )
    #             IngredientRecipe.objects.create(
    #                 recipe=recipe,
    #                 ingredient=current_ingredient,
    #                 amount=ingredient.get('amount')
    #             )
    #         for tag in tags:
    #             current_tag = get_object_or_404(
    #                 Tag,
    #                 id=tag.get('id')
    #             )
    #             recipe.tags.add(current_tag)
    #         return recipe


class RecipeWriteSerializer(RecipeSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def create(self, validated_data):
            validated_data.pop('ingredientrecipe_set')
            recipe = Recipe.objects.create(**validated_data)
            tags = self.initial_data.get('tags')
            ingredients = self.initial_data.get('ingredients')
            for ingredient in ingredients:
                current_ingredient = get_object_or_404(
                    Ingredient,
                    id=ingredient.get('id')
                )
                IngredientRecipe.objects.create(
                    recipe=recipe,
                    ingredient=current_ingredient,
                    amount=ingredient.get('amount')
                )
            for tag in tags:
                current_tag = get_object_or_404(
                    Tag,
                    id=tag
                )
                recipe.tags.add(current_tag)
            return recipe


class RecipeReducedSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
        model = Recipe


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор модели Follow."""
    email = serializers.ReadOnlyField(source='following.email')
    id = serializers.ReadOnlyField(source='following.id')
    username = serializers.ReadOnlyField(source='following.username')
    first_name = serializers.ReadOnlyField(source='following.first_name')
    last_name = serializers.ReadOnlyField(source='following.last_name')
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = RecipeReducedSerializer(many=True, source='following.recipes', read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        model = Follow
        read_only_fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        return self.context['request'].user.subscriptions.filter(
            following=obj.following
            ).exists()

    def get_recipes_count(self, obj):
        return obj.following.recipes.count()
