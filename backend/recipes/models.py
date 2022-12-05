from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


# class User(AbstractUser):
#     pass

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='Название ингредиента',
        help_text='Максимальная длина ингредиента 128 символов'
    )
    measurement_unit = models.CharField(
        max_length=16,
        verbose_name='Единица измерения',
        help_text='кг, г, шт, ст.л. и т.д.'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class IngredientRecipe(models.Model):
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        help_text='Количество ингридентов'
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

    def __str__(self):
        return f'{self.ingredient}, {self.recipe}'


class Tag(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='Название тега',
        help_text='Максимальная длина тега 128 символов'
    )
    color = models.CharField(
        max_length=16,
        verbose_name='Цвет тега',
        help_text='Цветовой HEX-код (например, #49B64E)'
        )
    slug = models.SlugField(max_length=128, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.slug


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        help_text='Автор рецепта'
    )
    name = models.CharField(
        max_length=128,
        verbose_name='Название рецепта',
        help_text='Максимальная длина названия 128 символов'
    )
    # image = models.ImageField('Изображение', upload_to='recipes/')
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
    tags = models.ManyToManyField('Tag', related_name='recipes')
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления рецепта',
        help_text='Время в минутах'
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
        return self.name
