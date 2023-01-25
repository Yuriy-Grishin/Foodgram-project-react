from django.core.management import BaseCommand

from csv import DictReader

from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Loads data from ingredients.csv"

    def handle(self, *args, **options):
        if Ingredient.objects.exists():
            print("ingredients data already loaded...exiting.")
            return
        print("Loading ingredients data")
        try:
            ingredients_dict = DictReader(open("../data/ingredients.csv"))
        except Exception:
            FileNotFoundError("Can't open file")
        try:
            for row in ingredients_dict:
                ing = Ingredient(
                    name=row["name"],
                    measurement_unit=row["measurement_unit"]
                )
                ing.save()
        except Exception:
            AttributeError("Can't save ingredient")
