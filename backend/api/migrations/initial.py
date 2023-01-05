import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                 serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True,
                 verbose_name='Название')),
                ('measurement_unit', models.CharField(max_length=150,
                 verbose_name='Единица измерения')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='IngredientQnt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                 serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(
                    validators=[django.core.validators.MinValueValidator(
                        1, message='Требуется больше 1!')],
                    verbose_name='Количество')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                 serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Имя')),
                ('image', models.ImageField(upload_to='recipes/',
                 verbose_name='Картинка')),
                ('text', models.TextField(max_length=200,
                 verbose_name='Описание')),
                ('cooking_time', models.PositiveSmallIntegerField(
                    validators=[django.core.validators.MinValueValidator(
                        1, message='Требуется больше 1 минуты')],
                    verbose_name='Время приготовления (минуты)')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                 serialize=False, verbose_name='ID')),
                ('name', models.CharField(
                    max_length=200, unique=True, verbose_name='Название')),
                ('color', models.CharField(max_length=7,
                 unique=True, verbose_name='Цвет')),
                ('slug', models.SlugField(
                    max_length=200, unique=True,
                    verbose_name='слаг')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                 serialize=False, verbose_name='ID')),
                ('recipe',
                 models.ForeignKey(
                                   on_delete=django.db.models.deletion.CASCADE,
                                   related_name='shoppinglist',
                                   to='recipes.recipe',
                                   verbose_name='Рецепт')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
