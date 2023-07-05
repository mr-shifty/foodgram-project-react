from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint

from users.models import User


class Ingredients(models.Model):
    name = models.CharField(
        "название ингредиента",
        max_length=100,
    )
    measurement_unit = models.CharField(
        'единица измерения',
        max_length=20
    )

    class Meta:
        ordering = ['name']
        verbose_name = "ингредиент"
        verbose_name_plural = "ингредиенты"

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="автор"
    )
    name = models.CharField(
        "название рецепта",
        max_length=200,
    )
    image = models.ImageField(
        "картинка",
        upload_to='recipes/images/',
        null=True,
        default=None
    )
    description = models.TextField(
        verbose_name="описание"
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name="ингредиенты"
    )
    tags = models.ManyToManyField(
        "Tags",
        related_name="recipes",
        verbose_name="теги"
    )
    cooking_time = models.PositiveSmallIntegerField(
        'время приготовления',
        validators=[
            MinValueValidator(1, message="Минимальное значение 1")
        ]
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_list',
        verbose_name='рецепт'
    )
    ingredients = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name='ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        'количество',
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
        verbose_name="название тега"
    )
    color = models.CharField(
        'цветовой HEX-код',
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
        "уникальный слаг",
        unique=True,
        max_length=200
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'избранный рецепт'
        verbose_name_plural = 'избранные рецепты'
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
        verbose_name="пользователь"
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name="рецепт"
    )

    class Meta:
        verbose_name = 'список покупок'
        verbose_name_plural = 'списки покупок'
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
