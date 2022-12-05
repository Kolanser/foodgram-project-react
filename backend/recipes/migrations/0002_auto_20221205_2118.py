# Generated by Django 3.2.15 on 2022-12-05 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, upload_to='recipes/', verbose_name='Изображение рецепта'),
        ),
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='amount',
            field=models.PositiveIntegerField(help_text='Количество ингридиентов', verbose_name='Количество'),
        ),
    ]