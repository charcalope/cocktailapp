from django import forms
from .data_utils import unit_choices

class CreateRecipeTagForm(forms.Form):
    description = forms.CharField(max_length=200)

class CreateRecipePartForm(forms.Form):
    amount = forms.CharField(max_length=5)
    unit = forms.ChoiceField(choices=unit_choices())
    ingredient = forms.CharField(max_length=100)

class CreateCocktailForm(forms.Form):
    cocktail_name = forms.CharField(max_length=200)
    cocktail_description = forms.CharField(max_length=400)
    cocktail_instructions = forms.CharField(max_length=400)
    cocktail_picture = forms.URLField(required=False)

class CreateIngredientForm(forms.Form):
    ingredient_name = forms.CharField(max_length=200)
    ingredient_aliases = forms.CharField(widget=forms.Textarea, label='Comma Separated List of aliases for ingredient')