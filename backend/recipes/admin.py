from django.contrib import admin
from django.contrib.admin import display

from .models import (
    Favorites, Ingredients, Recipe, RecipeIngredient, ShoppingCart, Tags,
)

from django.contrib import admin


# admin.site.register(Ingredients)

@admin.register(Ingredients)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Tags)
admin.site.register(Favorites)
admin.site.register(ShoppingCart)
