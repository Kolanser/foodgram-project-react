# Generated by Django 3.2.15 on 2022-12-05 14:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Максимальная длина ингредиента 128 символов', max_length=128, verbose_name='Название ингредиента')),
                ('measurement_unit', models.CharField(help_text='кг, г, шт, ст.л. и т.д.', max_length=16, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингридиент',
                'verbose_name_plural': 'Ингридиенты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(help_text='Количество ингридентов', verbose_name='Количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient', verbose_name='Ингридиент')),
            ],
            options={
                'verbose_name': 'Ингридиент и рецепт',
                'verbose_name_plural': 'Ингридиенты и рецепты',
                'ordering': ('recipe',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Максимальная длина тега 128 символов', max_length=128, verbose_name='Название тега')),
                ('color', models.CharField(help_text='Цветовой HEX-код (например, #49B64E)', max_length=16, verbose_name='Цвет тега')),
                ('slug', models.SlugField(max_length=128, unique=True)),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Максимальная длина названия 128 символов', max_length=128, verbose_name='Название рецепта')),
                ('description', models.TextField(blank=True, max_length=256, verbose_name='Описание рецепта')),
                ('cooking_time', models.PositiveIntegerField(help_text='Время в минутах', verbose_name='Время приготовления рецепта')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, help_text='Дата и время публикации', verbose_name='Дата публикации')),
                ('author', models.ForeignKey(help_text='Автор рецепта', on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('ingredients', models.ManyToManyField(related_name='recipes', through='recipes.IngredientRecipe', to='recipes.Ingredient', verbose_name='Ингридиенты')),
                ('tags', models.ManyToManyField(related_name='recipes', to='recipes.Tag')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.AddField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Рецепт'),
        ),
    ]
