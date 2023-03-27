import json
from django.core.management.base import BaseCommand
from recipes.models import Tag

"""Создаем команду по загрузке тегов в БД, выполняемую из командной строки с помощью скрипта manage.py"""
class Command(BaseCommand):

    def handle(self, *args, **options):
        """Выбираем путь нахождения данных и стандартный тип кодировки символов"""
        with open('data/tags.json', encoding='utf-8') as tagslist:
            tags = json.loads(tagslist.read())
            for tags in tags:
                Tag.objects.get_or_create(**tags)
        self.stdout.write('Теги загружены')