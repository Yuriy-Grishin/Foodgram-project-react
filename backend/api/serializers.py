from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from djoser.serializers import UserSerializer

from .utils.base64 import Base64ImageField
from recipes.models import (LikedRecipe, Product, Recipe, RecipeProduct, GroceryList, Tag)
from users.models import Subscriptions, User


class UsersListSerializer (serializers.ModelSerializer):
    """Сериалайзер показывает данные пользователей. Недоступно для анонимных посетителей сервиса"""
    usersubscriptions = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'username',
            'last_name',
            'email',
            'password',
            'id',
            'usersubscriptions',
        ]
    """Показывает подписки пользователя. Запрещено для анонимных пользователей"""
    def get_usersubscriptions(self, obj):
        site_visitor = self.context['request'].user
        if site_visitor.is_anonymous:
            return False
        return Subscriptions.objects.filter(
            user=site_visitor, author=obj).exists()


class CreateUserSerializer(serializers.ModelSerializer):
    """Сериалайзер создает нового пользователя"""
    class Meta:
        model = User
        """Кортеж защищает от изменений и может быть использован как ключ словаря"""
        fields = tuple(User.REQUIRED_FIELDS) + (User.USERNAME_FIELD, 'password')
        """Валидация имени пользователя"""
    def validate_username(self, value):
        if value == 'me':
            raise 'Невозможно создать пользователя с таким именем!'
        return value


class SubscriptionsListSerializer(UserSerializer):
    """Сериализатор для работы с подписками"""
    recipes = SerializerMethodField(read_only=True)
    recipes_count = SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('recipes', 'recipes_count')
 
    def get_recipes(self, object):
        context = {'request': self.context.get('request')}
        recipe_limit = self.context.get('request').query_params.get('recipe_limit')
        queryset = object.recipes.all()
        if recipe_limit:
            queryset = queryset[:int(recipe_limit)]
        return RecipeListSerializer(queryset, context=context, many=True).data

    def get_recipes_count(self, object):
        return object.recipes.count()


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для информации обо всех продуктах"""
    
    class Meta:
        model = Product    
        fields = ('id', 'name', 'measurement_unit')

    def __str__(self):
        return self.name


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериализатор для информации обо всех рецептах"""
    image = Base64ImageField(read_only=True)
    
    class Meta:
        model = Recipe
        fields = ['tags',
                  'author', 'products', 'name', 'image', 'text', 'cooking_time']


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с тегами."""

    class Meta:
        model = Tag
        fields = '__all__'


class ProductRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор связи продуктов и рецепта"""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    name = serializers.ReadOnlyField(source='product.name')
    measurement_unit = serializers.ReadOnlyField(
        source='product.measurement_unit'
    )

    class Meta:
        model = RecipeProduct
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeDetailsSerializer(serializers.ModelSerializer):
    """Сериализатор для детального описания рецепта"""
    author = UsersListSerializer(read_only=True)
    tags = TagSerializer(many=True)
    products = ProductRecipeSerializer(
        many=True, read_only=True, source='recipes')
    liked = serializers.SerializerMethodField(read_only=True)
    in_grocerylist = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'tags',
                  'author', 'products',
                  'liked', 'in_grocerylist',
                  'name', 'image',
                  'text', 'cooking_time']
 
    def get_image(self, obj):
        return obj.image.url

    def get_liked(self, object):
        user = self.context.get('request').user
        return LikedRecipe.objects.filter(user=user).exists()
 
    def get_in_grocerylist(self, object):
        user = self.context.get('request').user
        return GroceryList.objects.filter(user=user).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и редактирования данных рецепта"""
    products = ProductRecipeSerializer(many=True)
    author = UsersListSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    image = Base64ImageField(
        max_length=None,
        use_url=True,
    )

    class Meta:
        model = Recipe
        fields = (
            'name',
            'image',
            'text',
            'products',
            'tags',
            'cooking_time',
            'author'
        )

    def __str__(self):
        return self.name

    def create(self, info):
        tags = info.pop('tags')
        info_products = info.pop('products')
        recipe = Recipe.objects.create(
            name=info.pop('name'),
            author=self.context.get('request').user,
            text=info.pop('text'),
            cooking_time=info.pop('cooking_time'),
            image=info.pop('image')
        )
        recipe.tags.set(tags)
        for product in info_products:
            product_instance = product['id']
            amount = product['amount']
            RecipeProduct.objects.create(
                recipe=recipe, product=product_instance, amount=amount
            )
        return recipe
    
    def update(self, data, info):
        data.name = info.get('name', data.name)
        data.image = info.get('image', data.image)
        data.text = info.get('text', data.text)
        data.cooking_time = info.get(
            "cooking_time", data.cooking_time
        )

        tags = info.get('tags')
        if tags is not None:
            data.tags.clear()
            for tag in tags:
                data.tags.add(tag)

        products = info.get('products')
        if products is not None:
            RecipeProduct.objects.filter(recipe=data).all().delete()
            for product in products:
                product_id = product['id']
                amount = product['amount']
                RecipeProduct.objects.create(
                    recipe=data, product=product_id, amount=amount
                )
            data.save()
        return data
    
    def to_representation(self, instance):
        return RecipeDetailsSerializer(instance, context=self.context).data


class LikedRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с избранными рецептами."""
    class Meta:
        model = LikedRecipe
        fields = ('user', 'recipe')

    def validate(self, info):
        user = info['user']
        recipe = info['recipe']
        if self.Meta.model.objects.filter(user=user, recipe=recipe).exists():
            return info
    
    def to_representation(self, value):
        context = {'request': self.context.get('request')}
        return RecipeDetailsSerializer(value.recipe, context=context).info