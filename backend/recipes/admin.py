from django.contrib import admin

from recipes.models import Product, Tag, Recipe, RecipeProduct, LikedRecipe, GroceryList


admin.site.register(Product)


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "measurement_unit",
    )
    list_filter = ("name",)
    search_fields = ("name",)
    labels = {
        "name": "Название",
        "measurement_unit": "Единица измерения",
    }
    help_texts = {
        "name": "Наименование продуктов",
        "measurement_unit": "В чем измеряется продукт",
    }


admin.site.register(Recipe)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "author",
    )
    list_filter = (
        "name",
        "author",
        "tags",
    )
    labels = {
        "name": "Название",
        "author": "Автор",
        "tags": "Теги",
    }
    help_texts = {
        "name": "Наименование продуктв",
        "author": "Автор рецепта",
        "tags": "Теги рецепта",
    }


admin.site.register(RecipeProduct)


class RecipeProductAdmin(admin.ModelAdmin):
    list_display = (
        "recipe",
        "product",
        "amount",
    )
    labels = {
        "recipe": "Рецепт",
        "product": "Ингредиент",
        "amount": "Количество",
    }
    help_texts = {
        "recipe": "Рецепт, в который добавляется ингредиент",
        "product": "Ингредиент, который добавляется в рецепт",
        "amount": "Количество продукта, которое добавляется в рецепт",
    }


admin.site.register(LikedRecipe)


class LikedRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recipe",
    )
    labels = {
        "user": "Пользователь",
        "recipe": "Рецепт",
    }
    help_texts = {
        "user": "Пользователь в избранных рецептах",
        "recipe": "Рецепт в избранных",
    }


admin.site.register(Tag)


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    labels = {
        "name": "Наименование",
        "slug": "Слаг",
    }
    help_texts = {
        "name": "Наименование рецепта",
        "slug": "Слаг для поиска рецепта",
    }


admin.site.register(GroceryList)


class GroceryListAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recipe",
    )
    labels = {
        "user": "Пользователь",
        "recipe": "Рецепт",
    }
    help_texts = {
        "user": "Пользователь со списком покупок",
        "recipe": "Рецепт, по которому создается список покупок",
    }
