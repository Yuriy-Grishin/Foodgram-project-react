from django_filters.rest_framework import FilterSet, filters
from recipes.models import Product, Recipe, Tag


class ProductFilter(FilterSet):
    """Выбираем продукты по спецификатору начала названия без учета регистра"""

    name = filters.CharFilter(lookup_expr="istartswith")

    class Meta:
        model = Product
        fields = ("name",)


class RecipeFilter(FilterSet):
    """Выбираем рецепты по полям"""

    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug", to_field_name="slug", queryset=Tag.objects.all()
    )
    is_likedrecipe = filters.BooleanFilter(method="filter_is_likedrecipe")
    is_in_grocerylist = filters.BooleanFilter(method="is_in_grocerylist_filter")

    class Meta:
        model = Recipe
        fields = (
            "tags",
            "author",
        )

    """В списке избранных"""

    def filter_is_likedrecipe(self, queryset, name, data):
        user = self.request.user
        if data and user.is_authenticated:
            return queryset.filter(likedrecipe__user=user)
        return queryset

    """В списке покупок"""

    def is_in_grocerylist_filter(self, queryset, name, data):
        user = self.request.user
        if data and user.is_authenticated:
            return queryset.filter(grocerylist_recipe__user=user)
        return queryset
