from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import FileResponse

from rest_framework import status
from rest_framework.response import Response

from .models import Recipe, RecipeIngredient, ShoppingCart


@login_required
def shopping_cart(request, pk):
    if request.user.is_staff:
        instances = ShoppingCart.objects.filter(author_id=pk)
        shopping_list = []
        for instance in instances:
            recipe = Recipe.objects.get(name=instance.recipe)
            recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
            for ingredient in recipe_ingredients:
                shopping_list.append(
                    f"{ingredient.recipe}: {ingredient.ingredient.name}"
                    f" - {ingredient.amount}"
                )
        print(shopping_list)
        f = ContentFile('/n'.join(shopping_list))
        response = FileResponse(f.read(), content_type="text/plain")
        response[
            'Content-Disposition'
        ] = 'attachment; filename=shopping_cart.txt'
        return response
    return Response(status=status.HTTP_400_BAD_REQUEST)
