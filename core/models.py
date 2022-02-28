from django.db import models
from django.urls import reverse
from fuzzy_match import match
# Create your models here.

class IngredientAlias(models.Model):
    alias_name = models.CharField(max_length=200)

    def __str__(self):
        return self.alias_name

class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    aliases = models.ManyToManyField(IngredientAlias)

    def __str__(self):
        return self.name

    def match(self, raw_ingredient):
        raw_ingredient_l = raw_ingredient.lower()

        potential_matches = [self.name.lower()]

        for a in self.aliases.all():
            potential_matches.append(a.alias_name.lower())

        for pm in potential_matches:
            if pm in raw_ingredient_l:
                return True

        return False

class RecipePart(models.Model):
    amount = models.CharField(max_length=5)
    unit = models.CharField(max_length=15)
    raw_ingredient = models.CharField(max_length=100)

    tagged_ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return str(f"{self.amount} {self.unit} {self.raw_ingredient}")


class RecipeTag(models.Model):
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.description


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    picture = models.URLField(default='https://image.flaticon.com/icons/png/512/38/38706.png')
    description = models.CharField(max_length=400, default='No description set.')
    instructions = models.CharField(max_length=200, default='No instructions set.')

    recipe_parts = models.ManyToManyField(RecipePart)

    tags = models.ManyToManyField(RecipeTag)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('viewcocktail', kwargs={'pk': self.pk})

    def ingredient_match_score(self, search_space):
        scores = []
        typo_threshold = 0.5

        for recipe_part in self.recipe_parts.all():
            raw_ingredient = recipe_part.raw_ingredient
            result, score = match.extractOne(raw_ingredient, search_space)
            if score < typo_threshold:
                if result.lower() in raw_ingredient.lower():
                    score = 0.5
                else:
                    score = 0.0

            scores.append(score)

        weight = 100 / len(scores)
        weights = [weight for x in scores]

        zd = zip(weights, scores)
        weighted_scores = []
        for w, s in zd:
            weighted_scores.append(w*s)

        return sum(weighted_scores)


