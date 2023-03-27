from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from foodgram.settings import GROCERYLIST

from djoser.views import UserViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import Subscriptions, User
from recipes.models import (LikedRecipe, Product, Recipe, RecipeProduct,
                            GroceryList, Tag)
from api.filters import ProductFilter
from .pagination import LimitPagination
from .filters import RecipeFilter
from .permissions import IsAuthorOrReadOnly
from .serializers import UsersListSerializer, CreateUserSerializer, ProductSerializer, SubscriptionsListSerializer, LikedRecipeSerializer, RecipeListSerializer, TagSerializer, ProductRecipeSerializer, RecipeDetailsSerializer, RecipeCreateSerializer


class UsersListViewSet(UserViewSet):
    """Отображение пользователей и подписок"""
    queryset = User.objects.all()
    serializer_class = UsersListSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitPagination
    http_method_names = ['get', 'post', 'delete', 'head']

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

    """Определяем новый маршрут по подписке на автора с разрешенными методами для вьюсета с помощью декоратора action. Работа с конкретной записью"""
    @action(methods=['POST', 'DELETE'],
            detail=True, )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        subscription = Subscriptions.objects.filter(user=user, author=author)

        if request.method == 'POST':
            if subscription.exists():
                return Response({'error': 'Проверьте подписки! Этот автор уже в ваших подписках!'},
                                status=status.HTTP_409_CONFLICT)
            serializer = SubscriptionsListSerializer(author, context={'request': request})
            Subscriptions.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if subscription.exists():
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            
    """Определяем новый маршрут по подпискам с разрешенными методами для вьюсета с помощью декоратора action. Общий запрос без конкретной записи"""
    @action(detail=False, permission_classes=[IsAuthenticated])

    def subscriptions(self, request):
        user = request.user
        subscriptions = User.objects.filter(subscribed__user=user)
        page = self.paginate_queryset(subscriptions)
        serializer = SubscriptionsListSerializer(
            page, many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)

class CreateUserView(CreateAPIView):
    """Создаем пользователя"""
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CreateUserSerializer
    pagination_class = LimitPagination
    

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Создаем теги. Убираем паджинатор для корректной работы"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Создаем продукты. Убираем паджинатор для корректной работы. Ищем параметр по началу ^"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    search_fields = ('^name', )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    """Создаем рецепты. Убираем паджинатор для корректной работы. Ищем параметр по началу ^"""
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    pagination_class = LimitPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    search_fields = ('name',)
    
    """Выбираем тип сериализатора в зависимости от запроса"""
    def get_serializer_class(self):
        if self.action not in ('actions', 'retrieve'):
            return RecipeCreateSerializer 
        if self.action in ('actions', 'retrieve'):
            return RecipeDetailsSerializer

    def actions(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(
                page, many=True, context={'request': request}
            )
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(
            queryset, many=True, context={'request': request}
        )
        return Response(serializer.data)

    """Определяем новый маршрут по созданию/удалению рецепта с разрешенными методами для вьюсета с помощью декоратора action"""
    
    def makingrecipe(self, user, recipe_id, model):
        try:
            obj, created = model.objects.get_or_create(user=user, recipe_id=recipe_id)
        except ValidationError:
            print('Возникла ошибка')
        serializer_obj = Recipe.objects.get(pk=recipe_id)
        serializer = RecipeListSerializer(instance=serializer_obj)
        return Response(data=serializer.data)

    def deletingrecipe(self, user, recipe_id, model):
        model.objects.get(user, recipe_id).delete()
        return Response()

    """Определяем новый маршрут по созданию/удалению списка продуктов с разрешенными методами для вьюсета с помощью декоратора action. Работа с конкретной записью"""
    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )    
    def grocerylist(self, request, pk):
        if request.method == 'POST':
            try:
                GroceryList.objects.get(recipe_id=pk, user=request.user)
                return Response(data='Возникла ошибка')
            except Exception:
                return self.makingrecipe(user=request.user, recipe_id=pk, model=GroceryList)
        try:
            return self.deletingrecipe(user=request.user, recipe_id=pk, model=GroceryList)
        except ValidationError:
            print('Возникла ошибка')

    """Определяем новый маршрут по созданию/удалению из избранного с разрешенными методами для вьюсета с помощью декоратора action. Работа с конкретной записью"""
    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def likedrecipe(self, request, pk):
        if request.method == 'POST':
            return self.getliked(LikedRecipe, request.user, pk)
        if request.method == 'DELETE':
            return self.unlike(LikedRecipe, request.user, pk)
        
    def getliked(self, model, user, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeListSerializer(recipe)
        return Response(serializer.data)

    def unlike(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response()
                 
    """Определяем новый маршрут по выгрузке продуктов в список с разрешенными методами для вьюсета с помощью декоратора action. Общий запрос без конкретной записи"""
    @action(detail=False, methods=['GET'], permission_classes=(IsAuthenticated,))
    def download_grocerylist(self, request, **kwargs):
        """Выгружаем список продуктов для рецепта в формате txt"""
        products = (
            RecipeProduct.objects
            .filter(recipe__grocerylist_recipe__user=request.user)
            .values('product')
            .annotate(allproducts=Sum('amount'))
            .values_list('product__name', 'allproducts', 'product__measurement_unit')
        )
        productstobuy = []
        [productstobuy.append(
            '{}**********{}**********{}.'.format(*product)) for product in products]
        """Используем строковый метод format для вывода в каком хотим формате"""
        file = HttpResponse('Cписок покупок:\n\n\n\n' + ','.join(productstobuy),
                            content_type='text/plain')
        """Дсв елаем отступы. Методом join объяединяем список в строки. Простой текст"""
        file['Content-Disposition'] = (f'attachment; filename={GROCERYLIST}')
        """Устанавливаем заголовок Content-Disposition чтобы сервер отработал ответ как вложенный файл. Определяем местонахождение файла"""
        return file
    
