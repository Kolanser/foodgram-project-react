# Generated by Django 3.2.15 on 2022-12-09 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20221208_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(max_length=256, verbose_name='Описание рецепта'),
        ),
    ]
