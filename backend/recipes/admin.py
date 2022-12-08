from django.contrib import admin
from .models import CustomUser, Ingredient, IngredientRecipe, Tag, Recipe

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Админка ингридиентов."""
    list_display = (
        'email',
        'username',
        'first_name',
        'first_name',
        'password'
    )
    search_fields = ('username',)
    list_filter = ('username', 'email')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админка ингридиентов."""
    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    """Админка связей ингридиентов и рецептов."""
    list_display = (
        'recipe',
        'ingredient',
        'amount'
    )
    search_fields = ('recipe', 'ingredient')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админка тегов."""
    list_display = (
        'name',
        'color',
        'slug',
    )
    search_fields = ('name', 'slug')
    list_filter = (
        'name',
        'color',
        'slug',
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админка рецептов."""
    list_display = (
        'author',
        'name',
        'text',
        # 'ingredients',
        # 'tags',
        'cooking_time',
        'pub_date'
    )
    search_fields = ('name', 'author', 'tags')
    list_filter = ('name', 'tags', 'author')
    empty_value_display = '-пусто-'
