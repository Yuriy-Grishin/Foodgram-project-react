from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

from djoser.views import UserViewSet as DjoserUserViewSet

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientSearchFilter, RecipeSearchFilter
from .pagination import SixPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    FollowSerializer,
    IngredientSerializer,
    RecipeViewSerializer,
    RecipeWriteSerializer,
    ShortRecipeSerializer,
    TagSerializer
)
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag
)
from users.models import Subscriber, User


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        methods=["GET"],
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(
            id__in=Subscriber.objects.filter(user=request.user).values_list(
                "author_id", flat=True
            )
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FollowSerializer(
                page,
                many=True,
                context={
                    "request": request,
                },
            )
            return self.get_paginated_response(serializer.data)
        serializer = FollowSerializer(
            queryset,
            many=True,
            context={
                "request": request,
            },
        )
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["DELETE", "POST"],
        permission_classes=[IsAuthenticated],
        url_path="subscribe",
    )
    def subscribe(self, request, id):
        if request.method == "POST":
            author = User.objects.get(id=id)
            Subscriber.objects.get_or_create(author=author, user=request.user)
            author = User.objects.get(id=self.request.user.id)
            context = {"request": request}
            serializer = FollowSerializer(instance=author, context=context)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        author = User.objects.get(id=id)
        try:
            Subscriber.objects.filter(
                author=author, user=request.user
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    pagination_class = None
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientSearchFilter


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = SixPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeSearchFilter

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RecipeViewSerializer
        return RecipeWriteSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @transaction.atomic
    def create_instance(self, author, recipe_id, model):
        try:
            obj, created = model.objects.get_or_create(
                author=author,
                recipe_id=recipe_id
            )
        except IntegrityError:
            print("Integrity error occurs while handling transaction")
        if not created:
            raise ValidationError(f"{model.__class__.__name__} already exists")
        serializer_obj = Recipe.objects.get(pk=recipe_id)
        serializer = ShortRecipeSerializer(instance=serializer_obj)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def delete_instance(self, author, recipe_id, model):
        model.objects.get(author=author, recipe_id=recipe_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        if request.method == "POST":
            try:
                ShoppingCart.objects.get(recipe_id=pk, author=request.user)
                return Response(
                    data="Рецепт уже есть",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception:
                return self.create_instance(
                    author=request.user, recipe_id=pk, model=ShoppingCart
                )
        try:
            return self.delete_instance(request.user, pk, ShoppingCart)
        except Exception:
            return Response(
                data="рецепта отсутствует",
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(
        detail=False,
        methods=[
            "GET",
        ],
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        instances = ShoppingCart.objects.filter(author=request.user)
        shopping_list = []
        for instance in instances:
            recipe = Recipe.objects.get(name=instance.recipe)
            recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
            for ingredient in recipe_ingredients:
                shopping_list.append(
                    f"{ingredient.recipe}: {ingredient.ingredient.name}"
                    f" - {ingredient.amount}\n"
                )
        f = open("shopping_cart.txt", "w")
        for shopping in shopping_list:
            f.write(shopping)
        f.close()
        return HttpResponse(shopping_list, content_type="text/plain")

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        if request.method == "POST":
            try:
                Favorite.objects.get(recipe_id=pk, author=request.user)
                return Response(
                    data="Рецепт в избранном",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception:
                return self.create_instance(
                    author=request.user, recipe_id=pk, model=Favorite
                )
        try:
            return self.delete_instance(request.user, pk, Favorite)
        except Exception:
            return Response(
                data="рецепт отсутсвует в избранном",
                status=status.HTTP_400_BAD_REQUEST
            )
