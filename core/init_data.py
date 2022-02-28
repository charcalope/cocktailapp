from .models import Ingredient, Recipe, RecipePart
import pandas as pd

def init_ingredients():
    ingredient_names = []
    with open('core/data/ingredients_list.txt', 'r') as f:
        for line in f.readlines():
            if line.strip() not in ingredient_names:
                ingredient_names.append(line.strip())

    for i_name in ingredient_names:
        new_ingredient = Ingredient(name=i_name)
        new_ingredient.save()

def init_recipes():
    translations = dict()

    with open('core/data/ingredient_translations.txt', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            t_items = line.split(':::')

            t_dict = {'amount': t_items[1],
                      'unit': t_items[2],
                      'ingredient': t_items[3]}

            translations[t_items[0]] = t_dict

    df = pd.read_csv('core/data/cocktail_recipes.csv')
    recipe_dicts = df.to_dict('records')

    for recipe_dict in recipe_dicts:
        cocktail_name = recipe_dict['Cocktail Name']
        cocktail_instructions = recipe_dict['Preparation']

        raw_ingredients_description = recipe_dict['Ingredients']
        recipe_parts_strings = [x.strip() for x in raw_ingredients_description.split(',')]

        sanitary = True

        for recipe_parts_string in recipe_parts_strings:
            if recipe_parts_string not in translations.keys():
                sanitary = False

        if sanitary:
            new_recipe = Recipe(name=cocktail_name,
                                instructions=cocktail_instructions)

            new_recipe.save()

            for recipe_parts_string in recipe_parts_strings:
                t_dict = translations[recipe_parts_string]
                recipe_part_amount = t_dict['amount']
                recipe_part_unit = t_dict['unit']
                recipe_raw_ingredient = t_dict['ingredient']

                new_recipe_part = RecipePart(amount=recipe_part_amount,
                                             unit=recipe_part_unit,
                                             raw_ingredient=recipe_raw_ingredient)

                new_recipe_part.save()

                new_recipe.recipe_parts.add(new_recipe_part)

            new_recipe.save()

