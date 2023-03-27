from django.contrib import admin

from recipes.models import Product, Tag, Recipe, RecipeProduct, LikedRecipe, GroceryList


admin.site.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name', )
    search_fields = ('name', )


admin.site.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author',)
    list_filter = ('name', 'author', 'tags',)


admin.site.register(RecipeProduct)
class RecipeProductAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'product', 'amount',)


admin.site.register(LikedRecipe)
class LikedRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


admin.site.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


admin.site.register(GroceryList)
class GroceryListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)