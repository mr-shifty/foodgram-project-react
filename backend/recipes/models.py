from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint

from users.models import User


class Ingredients(models.Model):
    name = models.CharField(
        "Название ингредиента",
        max_length=100,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=20
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Ингредиент"
        verbose_name_plural = "Инредиенты"

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор"
    )
    name = models.CharField(
        "Название рецепта",
        max_length=200,
    )
    image = models.ImageField(
        "Картинка",
        upload_to='recipes/images/',
        null=True,
        default=None
    )
    description = models.TextField(
        verbose_name="Описание"
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name="Ингредиенты"
    )
    tags = models.ManyToManyField(
        "Tags",
        related_name="recipes",
        verbose_name="Теги"
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[
            MinValueValidator(1, message="Минимальное значение 1")
        ]
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_list',
        verbose_name='Рецепт'
    )
    ingredients = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[
            MinValueValidator(1, 'Минимальное количество 1')
        ]
    )

    class Meta:
        verbose_name = "Ингредиент в рецепте",
        verbose_name_plural = "Ингредиенты в рецептах"

    def __str__(self):
        return (
            f'{self.ingredients.name} ({self.ingredients.measurement_unit})'
            f'- {self.amount}'
        )


class Tags(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название тега"
    )
    color = models.CharField(
        'Цветовой HEX-код',
        unique=True,
        max_length=7,
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Введенное значение не является цветом в формате HEX!'
            )
        ]
    )
    slug = models.SlugField(
        "Уникальный слаг",
        unique=True,
        max_length=200
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='uq_user_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил "{self.recipe}" в Избранное'

    @classmethod
    def add_favorite(cls, user, recipe):
        favorite, created = cls.objects.get_or_create(user=user, recipe=recipe)
        return favorite

    @classmethod
    def remove_favorite(cls, user, recipe):
        cls.objects.filter(user=user, recipe=recipe).delete()


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        verbose_name="Пользователь"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name="рецепт"
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='uq_user_reciepe'
            ),
            CheckConstraint(
                check=~models.Q(user=models.F('recipe')),
                name='prevent_self_favorite',
            )
        ]

    def __str__(self) -> str:
        return f'{self.user} добавил "{self.recipe}" в Список покупок'
