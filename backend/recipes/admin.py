from .models import (
    Favorites, Ingredients, Recipe, RecipeIngredient, ShoppingCart, Tags,
)

from django.contrib import admin


admin.site.register(Ingredients)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Tags)
admin.site.register(Favorites)
admin.site.register(ShoppingCart)
