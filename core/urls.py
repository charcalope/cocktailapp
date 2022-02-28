from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    # INGREDIENTS
    path('ingredients/<pk>', views.view_ingredient, name='viewingredient'),
    path('ingredients/create/', views.create_ingredient, name='createingredient'),
    path('ingredients/all/', views.ingredient_directory, name='allingredients'),
    # COCKTAILS
    path('cocktails/<pk>', views.view_cocktail, name='viewcocktail'),
    path('cocktails/all/', views.cocktail_directory, name='allcocktails'),
    path('cocktails/create/', views.create_cocktail, name='createcocktail'),
    path('cocktails/<pk>/recipe/', views.view_recipe, name='viewrecipe'),
    path('cocktails/<pk>/newrecipepart/', views.new_recipe_part, name='newrecipepart'),
    path('cocktails/<pk>/edit', views.CocktailUpdateView.as_view(), name='editcocktail'),
    path('cocktails/parts/<pk>/edit', views.edit_recipe_part_tags, name='editparttags'),
    path('cocktails/parts/<recipe_part_id>/add/<ingredient_id>', views.add_tag_to_recipe_part, name='addparttag'),
    path('cocktails/parts/<recipe_part_id>/remove/<ingredient_id>', views.delete_tag_from_recipe_part, name='removeparttag'),
    path('makedrinks/', views.make_drinks, name='makedrinks'),
    path('cocktails/<pk>/recipe/tags/', views.search_for_general_recipe_tags, name='searchrecipetag'),
    path('cocktails/<recipe_pk>/recipe/tags/<tag_pk>/add', views.add_general_tag_to_recipe, name='addrecipetag'),
    path('cocktails/<pk>/recipe/tags/new', views.define_new_tag, name='newrecipetag'),
]