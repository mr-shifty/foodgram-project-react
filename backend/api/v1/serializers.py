from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (
    Favorite, Ingredient, Recipe,
    RecipeIngredient, ShoppingCart, Tag)
from .users.serializers import UserSerializer


class TagsSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор связи инредиента и рецепта."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра рецептов."""

    tags = TagsSerializer(read_only=False, many=True)
    author = UserSerializer(read_only=True, many=False)
    ingredients = RecipeIngredientSerializer(
        many=True, source='ingredient_list'
    )
    is_favorite = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(max_length=None)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorite', 'is_in_shopping_cart', 'name',
            'image', 'description', 'cooking_time'
        )

    def get_recipe(self, obj):
        ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return RecipeIngredientSerializer(ingredients, many=True).data

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.favorites.filter(user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.shopping_cart.filter(user=request.user).exists()


class CreateRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор создания рецепта."""

    ingredients = RecipeIngredientSerializer(
        many=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        error_messages={'does_not_exist': 'Данного тега не существует'}
    )
    image = Base64ImageField(max_length=None)
    author = UserSerializer(read_only=True)
    coocking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'coocking_time'
        )

    def validate_tags(self, tags):
        non_existing_tags = tags.exclude(
            id__in=Tag.objects.values_list('id', flat=True)
        )
        if non_existing_tags.exists():
            raise serializers.ValidationError('Данного тега не существует')
        return tags

    def validate_coocking_time(self, coocking_time):
        if coocking_time < 1:
            raise serializers.ValidationError(
                'Время приготовления не может быть меньше 1 минуты'
            )
        return coocking_time

    def validate_ingredients(self, ingredients):
        ingredients_list = []
        if not ingredients:
            raise serializers.ValidationError(
                'Отсутсвуют ингредиенты'
            )
        for ingredient in ingredients:
            if ingredient[id] in ingredients_list:
                raise serializers.ValidationError(
                    'Ингредиеты должны быть уникальными'
                )
            ingredients_list.append(ingredient[id])
            if int(ingredient.get('amount')) < 1:
                raise serializers.ValidationError(
                    "Количество ингредиентов должно быть больше 0"
                )
        return ingredients

    @staticmethod
    def create_ingredients(recipe, ingredients):
        ingredient_liist = []
        for ingredient_data in ingredients:
            ingredient_liist.append(
                RecipeIngredient(
                    ingredient=ingredient_data.pop('id'),
                    amount=ingredient_data.pop('amount'),
                    recipe=recipe,
                )
            )
        RecipeIngredient.objects.bulk_create(ingredient_liist)

    def create(self, validated_data):
        request = self.context.get('request', None)
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        RecipeIngredient.objects.filter(recipe=instance).delete()
        instance.tags.set(validated_data.pop('tags'))
        ingredients = validated_data.pop('ingredients')
        self.create_ingredients(instance, ingredients)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context={
            'request': self.context.get('request')
        }).data


class RecipeShortSerializer(serializers.ModelSerializer):
    """ Сериализатор полей избранных рецептов и покупок."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор избранного."""

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        user = data['user']
        if user.favorites.filter(recipe=data['recipe']).exists():
            raise serializers.ValidationError(
                'Рецепт уже добавлен в избранное.'
            )
        return data

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор списка покупок."""

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')

    def validate(self, data):
        user = data['user']
        if user.shopping_list.filter(recipe=data['recipe']).exists():
            raise serializers.ValidationError(
                'Рецепт уже добавлен в корзину'
            )
        return data

    def to_representation(self, instance):
        return RecipeShortSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data
