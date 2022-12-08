from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


# Минимальное время приготовления рецепта
MIN_VALUE_COOKING_TIME: int = 1


class CustomUser(AbstractUser):
    """Модель пользователя."""
    first_name = models.CharField('first name', max_length=150, unique=True)
    last_name = models.CharField('last name', max_length=150, unique=True)
    email = models.EmailField('email address', unique=True)
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']


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
        return f'{self.ingredient}, {self.recipe}'


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега',
        help_text='Максимальная длина тега 200 символов'
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
        CustomUser,
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
        blank=True,
        help_text='Картинка, закодированная в Base64'
    )
    description = models.TextField(
        max_length=256,
        blank=True,
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
