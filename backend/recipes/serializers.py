from django.shortcuts import get_object_or_404
from rest_framework import serializers
from drf_base64.fields import Base64ImageField

from users.models import Follow
from .models import (
    Favorite, Ingredient, Recipe, ShoppingCart, Tag, RecipeIngredient
)
from .models import User


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient
        read_only_fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag
        read_only_fields = ('id', 'name', 'color', 'slug')


class AuthorSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user, author=obj.pk).exists()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed'
        )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient.id', queryset=Ingredient.objects.all()
    )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True
    )
    name = serializers.CharField(
        source='ingredient.name', read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        queryset = RecipeIngredient.objects.filter(recipe=obj)
        return RecipeIngredientSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user.id, recipe=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=user.id,
            recipe=obj.id
        ).exists()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )


class IngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientCreateSerializer(many=True)
    image = Base64ImageField()

    def to_representation(self, instance):
        request = self.context.get('request')
        serializer = RecipeListSerializer(
            instance,
            context={'request': request}
        )
        return serializer.data

    def validate(self, data):
        ingredient_data = self.initial_data.get('ingredients')
        if ingredient_data:
            checked_ingredients = set()
            for ingredient in ingredient_data:
                ingredient_obj = get_object_or_404(
                    Ingredient, id=ingredient['id']
                )
                if ingredient_obj in checked_ingredients:
                    raise serializers.ValidationError('ингредиент дублируется')
                checked_ingredients.add(ingredient_obj)
        return data

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )


class FollowRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
