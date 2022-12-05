from csv import DictReader
from json import load
from django.core.management import BaseCommand
import logging
import sys

from ...models import Ingredient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s, [%(levelname)s] %(message)s'
)
handler.setFormatter(formatter)


class Command(BaseCommand):
    help = 'Загрузка данных в БД'

    def handle(self, *args, **options):
        logger.info('Удаление данных в таблице Ингридиенты')
        Ingredient.objects.all().delete()

        logger.info('Загрузка ингридиентов в БД')
        ingredients = []
        for row in DictReader(
            open('./data/ingredients.csv', encoding='utf-8'),
            ['name', 'measurement_unit']
        ):
            ingredients.append(
                Ingredient(
                    name=row['name'],
                    measurement_unit=row['measurement_unit'],
                )
            )

        Ingredient.objects.bulk_create(ingredients)

        logger.info('Загрузка ингридиентов в БД завершена')
