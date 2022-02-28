from core.models import Ingredient
from fuzzy_match import match


def search_ingredients(query):
    id_mapping = dict()

    ingredients = Ingredient.objects.all()

    for i in ingredients:
        i_id = str(i.pk)
        id_mapping[i.name] = i_id

        for alias in i.aliases.all():
            id_mapping[alias.alias_name] = i_id

    search_space = list(id_mapping.keys())

    results = match.extract(query, search_space, limit=5, score_cutoff=0.1)

    target_ids = []

    for result, score in results:
        target_id = id_mapping[result]
        if target_id not in target_ids:
            target_ids.append(target_id)

    return target_ids

