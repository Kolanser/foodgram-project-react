from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model


# Минимальное время приготовления рецепта
MIN_VALUE_COOKING_TIME: int = 1

User = get_user_model()


class Ingredient(models.Model):
    """Модель ингридиентов."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
        help_text='Максимальная длина ингредиента 200 символов'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
        help_text='кг, г, шт, ст.л. и т.д.'
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            models.UniqueConstraint(
                name='unique_ingredients',
                fields=['name', 'measurement_unit'],
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class IngredientRecipe(models.Model):
    """Модель для связи ингридиентов и рецептов."""
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        help_text='Количество ингридиентов'
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        verbose_name='Ингридиент',
        # related_name='ingredients_for_recipe'
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Ингридиент и рецепт'
        verbose_name_plural = 'Ингридиенты и рецепты'
        constraints = [
            models.UniqueConstraint(
                name='unique_ingredients_for_recipe',
                fields=['ingredient', 'recipe'],
            )
        ]

    def __str__(self):
        return f'{self.ingredient}, {self.amount}, {self.recipe}'


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега',
        help_text='Максимальная длина тега 200 символов',
        unique=True
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет тега',
        help_text='Цветовой HEX-код (например, #49B64E)'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.slug


class Recipe(models.Model):
    """Модель рецептов."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        help_text='Автор рецепта'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Максимальная длина названия 200 символов'
    )
    image = models.ImageField(
        verbose_name='Изображение рецепта',
        upload_to='recipes/',
        help_text='Картинка, закодированная в Base64'
    )
    text = models.TextField(
        max_length=256,
        verbose_name='Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='IngredientRecipe',
        related_name='recipes',
        verbose_name='Ингридиенты'
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления рецепта',
        help_text='Время приготовления (в минутах)',
        validators=[MinValueValidator(MIN_VALUE_COOKING_TIME)]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Дата и время публикации',
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name}, {self.author}'


class Favorite(models.Model):
    """Модель избранного."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Пользователь',
        help_text='Пользователь, который добавил рецепт в избранное'
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='favorited',
        verbose_name='Рецепт',
        help_text='Рецепт в избранном'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                name='unique_favorites',
                fields=['user', 'recipe'],
            )
        ]


class ShoppingCart(models.Model):
    """Модель списка покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='Пользователь',
        help_text='Пользователь, который добавил рецепт в список покупок'
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='in_shopping_cart',
        verbose_name='Рецепт',
        help_text='Рецепт в списке покупок'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                name='unique_shopping_carts',
                fields=['user', 'recipe'],
            )
        ]
