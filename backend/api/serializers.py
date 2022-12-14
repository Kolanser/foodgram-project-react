from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from djoser.conf import settings
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from rest_framework import serializers
from users.models import Follow

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор для пользователя."""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
        ) + ('is_subscribed', )
        read_only_fields = (settings.LOGIN_FIELD, 'is_subscribed')

    def get_is_subscribed(self, obj):
        """Подписан ли текущий пользователь на этого."""
        user = self.context['request'].user
        return (
            user.is_authenticated
            and user.subscriptions.filter(following=obj).exists()
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient
        read_only_fields = ('name',)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag
        read_only_fields = ('name', 'color', 'slug')


class IdIngredientField(serializers.Field):
    """Поле для id в модели связей ингредиентов и рецептов."""
    def to_representation(self, value):
        """Предоставить значение без преобразования."""
        return value

    def to_internal_value(self, data):
        """Проверить наличие ингредиента и вернуть id."""
        get_object_or_404(Ingredient, id=data)
        return data


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор связей ингредиентов и рецептов."""
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    id = IdIngredientField(source='ingredient.id')

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
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)

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
            'is_favorited',
            'is_in_shopping_cart'
        )
        model = Recipe
        read_only_fields = ('id',)

    def get_is_favorited(self, obj):
        """Находится ли рецепт в списке избранного."""
        user = self.context['request'].user
        return (
            user.is_authenticated
            and user.favorite_recipes.filter(
                recipe=obj
            ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        """Находится ли рецепт в списке покупок."""
        user = self.context['request'].user
        return (
            user.is_authenticated
            and user.shopping_carts.filter(
                recipe=obj
            ).exists()
        )


class RecipeWriteSerializer(RecipeSerializer):
    """Сериализатор для создания и изменения рецепта."""
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    @transaction.atomic
    def create(self, validated_data):
        """Создание рецепта."""
        ingredients_recipe = validated_data.pop('ingredientrecipe_set')
        tags = validated_data.pop('tags')
        recipe = super().create(validated_data)
        recipe.tags.set(tags)
        ingredients_amount = []
        for ingredient_recipe in ingredients_recipe:
            id = ingredient_recipe['ingredient'].get('id')
            ingredients_amount.append(
                IngredientRecipe(
                    recipe=recipe,
                    ingredient=Ingredient.objects.get(id=id),
                    amount=ingredient_recipe.get('amount')
                )
            )
        IngredientRecipe.objects.bulk_create(ingredients_amount)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        """Обновление рецепта."""
        tags = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredientrecipe_set')
        instance = super().update(instance, validated_data)
        instance.tags.set(tags)
        instance.ingredients.clear()
        ingredients_amount = []
        for ingredient in ingredients_data:
            id = ingredient['ingredient'].get('id')
            current_ingredient = get_object_or_404(
                Ingredient,
                id=id
            )
            ingredients_amount.append(
                IngredientRecipe(
                    recipe=instance,
                    ingredient=current_ingredient,
                    amount=ingredient.get('amount')
                )
            )
        IngredientRecipe.objects.bulk_create(ingredients_amount)
        return instance

    def to_representation(self, instance):
        """Для показа данных о новом рецепте."""
        return RecipeSerializer(
            instance,
            context={
                'request': self.context.get('request'),
            }
        ).data


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
    recipes = serializers.SerializerMethodField()
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

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        recipes = obj.following.recipes.all()
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        serializer = RecipeReducedSerializer(
            recipes,
            many=True,
            read_only=True
        )
        return serializer.data
