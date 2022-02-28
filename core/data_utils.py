from .models import Ingredient, IngredientAlias

def unit_choices():
    return (
        ('Unit', 'Unit'),
        ('oz', 'oz')
    )

def match_to_ingredient_ids(raw_ingredient):
    ingredients = Ingredient.objects.all()

    matched_ingredients_ids = []

    for i in ingredients:
        if i.match(raw_ingredient):
            matched_ingredients_ids.append(i.pk)

    return matched_ingredients_ids
