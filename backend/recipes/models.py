from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Product(models.Model):
    name = models.CharField(
        'Продукт',
        max_length=40
    )
    measurement_unit = models.CharField(
        'Единица измерения продукта',
        max_length=40
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(
        max_length=40,
        unique=True
    )
    slug = models.SlugField(
        max_length=40,
        verbose_name='Slug',
        unique=True
    )

    class Meta:
        ordering = ['-name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    name = models.CharField(
        'Блюдо',
        max_length=40
    )
    text = models.CharField(
        'Описание процедуры приготовления блюда',
        max_length=4000,
    )
    cooking_time = models.PositiveIntegerField(
        ('Время приготовления рецепта'),
        validators=[MinValueValidator(limit_value=5,
                    message=("Хорошее блюдо за 5 минут не приготовишь!")), 
                    MaxValueValidator(limit_value=200,
                    message=("Слишком долго! Может лучше заказать?"))])
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
    )
    pub_date = models.DateTimeField(
        'Дата публикации блюда',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recipes',
        verbose_name='Автор блюда'
    )
    products = models.ManyToManyField(
        Product,
        through='RecipeProduct',
        through_fields=('recipe', 'product'),
        verbose_name='Продукты'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.name


class RecipeProduct(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Блюда'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Продукт',
    )
    amount = models.PositiveIntegerField(
        ('Количество'),
        validators=[MinValueValidator(limit_value=0.000001,
                    message=("Нулевок значение недопустимо!")), 
                    MaxValueValidator(limit_value=999999,
                    message=("Готовишь для большой компании? Слишком много продуктов даже для компании! "))])

    class Meta:
        verbose_name = 'Продукт в рецепте'
        verbose_name_plural = 'Продукты в рецептах'
        constraints = [models.UniqueConstraint(
                fields=['recipe', 'product'],
                name='unique'
               )
        ]

    def __str__(self):
        return 'Продукты в рецепте'


class LikedRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='likedrecipe'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепты',
        related_name='likedrecipe'
    )

    class Meta:
        ordering = ['-user']
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'



class GroceryList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='grocerylist_user',
        verbose_name='В списке'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='grocerylist_recipe',
        verbose_name='В списке покупок'
    )

    class Meta:
        ordering = ['-recipe']
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'

    def __str__(self):
        return 'Список покупок'