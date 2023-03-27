import json
from django.core.management.base import BaseCommand
from recipes.models import Product

"""Создаем команду по загрузке продуктов в БД, выполняемую из командной строки с помощью скрипта manage.py"""
class Command(BaseCommand):

    def handle(self, *args, **options):
        """Выбираем путь нахождения данных и стандартный тип кодировки символов"""
        with open('data/products.json', encoding='utf-8') as products_list:
            for products in json.loads(products_list.read()):
                Product.objects.get_or_create(**products)
        self.stdout.write('Продукты загружены')
