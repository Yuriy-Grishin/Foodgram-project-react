from django.contrib import admin

from recipes.models import (
    Ingredient, Recipe, Tag, RecipeIngredient, ShoppingCart, Favorite
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color')
    list_editable = ('color',)
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name', )
    list_display_links = ('name',)
    search_fields = ('name', )
    empty_value_display = '-пусто-'


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'text',
                    'cooking_time', 'pub_date',)
    search_fields = ('name', )
    ordering = ('-pub_date',)
    inline = (RecipeIngredientInline, )
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-empty-'
    readonly_fields = ['favorited_count']

    def favorited_count(self, obj):
        return obj.favorites_recipe.count()


@admin.register(RecipeIngredient)
class RecipeAdminIngredient(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    list_display_links = ('recipe',)
    search_fields = ('recipe',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_display_links = ('user',)
    search_fields = ('user',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_display_links = ('user',)
    search_fields = ('user',)
