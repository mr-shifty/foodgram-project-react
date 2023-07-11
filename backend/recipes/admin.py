from django.contrib import admin
from .models import (
    Favorites, Ingredients, Recipe,
    RecipeIngredient, ShoppingCart, Tags, )


@admin.register(Ingredients)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'id')
    list_filter = ('author', 'name', 'tags')


@admin.register(RecipeIngredient)
class IngredientInRecipe(admin.ModelAdmin):
    list_display = ('recipe', 'ingredients', 'amount',)


@admin.register(Tags)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)


@admin.register(Favorites)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
