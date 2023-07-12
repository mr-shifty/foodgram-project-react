from django.contrib import admin
from django.db.models import Count

from .models import (
    Favorite, Ingredient, Recipe, RecipeIngredient, ShoppingCart, Tag,
)


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 3
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author', 'name', 'cooking_time', 'get_favorites', 'get_ingredients',
    )
    search_fields = ('name', 'author__username', 'tags__name')
    list_filter = ('author__username', 'name', 'tags__name',)
    inlines = (IngredientInline,)
    empty_value_display = '-пусто-'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('author')
        queryset = queryset.prefetch_related('ingredients', 'tags')
        queryset = queryset.annotate(favorites_count=Count('favorites'))
        return queryset

    def get_favorites(self, obj):
        return obj.favorites_count
    get_favorites.short_description = 'Избранное'

    def get_ingredients(self, obj):
        return ', '.join(
            [ingredient.name for ingredient in obj.ingredients.all()]
        )
    get_ingredients.short_description = 'Ингредиенты'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """ Админ панель управление ингридиентами. """

    list_display = ('name', 'measurement_unit')
    search_fields = ('name', )
    list_filter = ('name', )
    empty_value_display = '-пусто-'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """ Админ панель управление рецепты и инредиенты. """

    list_display = ('recipe', 'ingredients', 'amount',)
    search_fields = ('recipe', )
    list_filter = ('recipe', )
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """ Админ панель управление тегами. """

    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', )
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """ Админ панель управление подписками. """

    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """ Админ панель списка покупок. """

    list_display = ('recipe', 'user')
    list_filter = ('recipe', 'user')
    search_fields = ('user', )
    empty_value_display = '-пусто-'
