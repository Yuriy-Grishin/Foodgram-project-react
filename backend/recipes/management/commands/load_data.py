import csv
import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class Command(BaseCommand):
    def handle(self, *args, **options):
        Ingredient.objects.all().delete()
        logging.info(' Модель Ingredient стерта.')
        data_path = settings.BASE_DIR
        with open(
            f'{data_path}/data/ingredients.csv',
            'r',
            encoding='utf-8'
        ) as file:
            reader = csv.reader(file)
            counter = 0
            for row in reader:
                if counter % 100 == 0:
                    logging.info(f' Добавлен  {row[0]}')
                ingr = Ingredient.objects.create(name=row[0], measurement_unit=row[1])
                ingr.save()
                counter += 1
        logging.info(
            f' Добавлено - {counter} строк'
        )
