# Generated by Django 3.2.15 on 2022-12-21 20:13

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Максимальная длина ингредиента 200 символов', max_length=200, verbose_name='Название ингредиента')),
                ('measurement_unit', models.CharField(help_text='кг, г, шт, ст.л. и т.д.', max_length=200, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингридиент',
                'verbose_name_plural': 'Ингридиенты',
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(help_text='Количество ингридиентов', verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Ингридиент и рецепт',
                'verbose_name_plural': 'Ингридиенты и рецепты',
                'ordering': ('recipe',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Максимальная длина названия 200 символов', max_length=200, verbose_name='Название рецепта')),
                ('image', models.ImageField(help_text='Картинка, закодированная в Base64', upload_to='recipes/', verbose_name='Изображение рецепта')),
                ('text', models.TextField(max_length=256, verbose_name='Описание рецепта')),
                ('cooking_time', models.PositiveIntegerField(help_text='Время приготовления (в минутах)', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления рецепта')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, help_text='Дата и время публикации', verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Максимальная длина тега 200 символов', max_length=200, unique=True, verbose_name='Название тега')),
                ('color', models.CharField(help_text='Цветовой HEX-код (например, #49B64E)', max_length=7, verbose_name='Цвет тега')),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(help_text='Рецепт в списке покупок', on_delete=django.db.models.deletion.CASCADE, related_name='in_shopping_cart', to='recipes.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Список покупок',
                'verbose_name_plural': 'Списки покупок',
            },
        ),
    ]
