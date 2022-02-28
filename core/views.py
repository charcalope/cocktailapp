from django.http import HttpResponse, request
from django.shortcuts import render, redirect
from .models import Recipe, Ingredient, IngredientAlias, RecipePart, RecipeTag
from .forms import CreateCocktailForm, CreateIngredientForm, CreateRecipePartForm, CreateRecipeTagForm
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .data_utils import match_to_ingredient_ids
from cabinet.search_utils import search_ingredients
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Hello, if you're from AirBnB or just stumbled upon this repo
# This is part of a project I made for my boyfriend, a budding home bartender
# to aid in finding drinks he could make with what he had on hand.

# I never thought anybody else would see this, and comments may be incomplete
# Given that I'm struggling through an active COVID-19 infection...
# It was the best coding sample I had readily available

# As I may not even get an interview,
# I had a lot of fun preparing for this - I learned Swift for my intended project before I got sick
# and the essay questions were really interesting

@login_required
def make_drinks(request):
    # fetch the set of ingredients this user has on hand (cabinet)
    # and common aliases for those ingredients
    search_space = request.user.ingredient_set_with_aliases()
    # fetch all possible cocktail recipes
    cocktails = Recipe.objects.all()
    # for every cocktail recipe, assign a score
    # the more ingredients from that recipe the user has, the higher the score
    cocktail_scores = [cocktail.ingredient_match_score(search_space) for cocktail in cocktails]
    zd = list(zip(cocktails, cocktail_scores))
    zd.sort(key=lambda x: x[1], reverse=True)

    results = []

    for cocktail, score in zd:
        result = dict()
        result['cocktail'] = cocktail
        result['score'] = str(f"{int(score)}%")
        results.append(result)

    paginator = Paginator(results, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cocktails/make_drinks.html', {'page_obj': page_obj})


def index(request):
    return render(request, 'final_home.html', {})

def cocktail_directory(request):
    cocktails = Recipe.objects.all()
    paginator = Paginator(cocktails, 20)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cocktails/cocktail_directory.html', {'page_obj': page_obj})

def view_cocktail(request, pk):
    cocktail = Recipe.objects.get(pk=pk)
    return render(request, 'cocktails/view_cocktail.html', {'cocktail': cocktail})

def view_recipe(request, pk):
    cocktail = Recipe.objects.get(pk=pk)
    return render(request, 'cocktails/view_recipe.html', {'cocktail': cocktail})

def new_recipe_part(request, pk):
    cocktail = Recipe.objects.get(pk=pk)
    if request.method == 'POST':
        form = CreateRecipePartForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # define new recipe part object
            recipe_amount = data['amount']
            recipe_unit = data['unit']
            recipe_ingredient = data['ingredient']

            new_recipe_part_object = RecipePart(amount=recipe_amount,
                                                unit=recipe_unit,
                                                raw_ingredient=recipe_ingredient)

            new_recipe_part_object.save()

            # tag new recipe part object with relevant ingredients

            # define relevant ingredients to this recipe part
            # to aid in faster search function (comparing to cabinet ingredients)
            pending_tagged_ingredients = match_to_ingredient_ids(recipe_ingredient)

            # check if no matches were found
            if len(pending_tagged_ingredients) > 0:
                for pending_tagged_ingredient_id in pending_tagged_ingredients:
                    pending_ingredient = Ingredient.objects.get(pk=pending_tagged_ingredient_id)
                    new_recipe_part_object.tagged_ingredients.add(pending_ingredient)
            else:
                # create new ingredient
                new_ingredient = Ingredient(name=recipe_ingredient)
                new_ingredient.save()

                new_recipe_part_object.tagged_ingredients.add(new_ingredient)

            new_recipe_part_object.save()

            # add to parent recipe
            cocktail.recipe_parts.add(new_recipe_part_object)

            cocktail.save()

            return redirect('viewcocktail', pk=cocktail.pk)
    else:
        form = CreateRecipePartForm()
    return render(request, 'cocktails/new_recipe_part.html', {'form': form})

def create_cocktail(request):
    if request.method == 'POST':
        form = CreateCocktailForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            cocktail_name = data['cocktail_name']
            cocktail_description = data['cocktail_description']
            cocktail_instructions = data['cocktail_instructions']

            new_cocktail = Recipe(name=cocktail_name,
                                  description=cocktail_description,
                                  instructions=cocktail_instructions)

            new_cocktail.save()

            if data['cocktail_picture']:
                cocktail_picture = data['cocktail_picture']
                new_cocktail.picture = cocktail_picture
                new_cocktail.save()

            # then redirect to view recipe
            return redirect('viewrecipe', pk=new_cocktail.pk)
    else:
        form = CreateCocktailForm()
    return render(request, 'cocktails/create_cocktail.html', {'form': form})

def ingredient_directory(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'cocktails/ingredient_directory.html', {'ingredients': ingredients})

def view_ingredient(request, pk):
    ingredient = Ingredient.objects.get(pk=pk)
    return render(request, 'cocktails/post_create_ingredient.html', {'ingredient': ingredient})

def create_ingredient(request):
    if request.method == 'POST':
        form = CreateIngredientForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ingredient_name = data['ingredient_name']
            new_ingredient = Ingredient(name=ingredient_name)
            new_ingredient.save()

            raw_aliases = data['ingredient_aliases'].split(',')
            aliases = []
            for alias in raw_aliases:
                new_alias = IngredientAlias(alias_name=alias)
                new_alias.save()
                new_ingredient.aliases.add(new_alias)

            new_ingredient.save()
            return redirect('viewingredient', pk=new_ingredient.pk)
    else:
        form = CreateIngredientForm()
    return render(request, 'cocktails/create_ingredient.html', {'form': form})


class CocktailUpdateView(UpdateView):
    model = Recipe
    fields = ['name', 'picture', 'description', 'instructions']
    template_name = 'cocktails/edit_cocktail.html'

def edit_recipe_part_tags(request, pk):
    recipe_part = RecipePart.objects.get(pk=pk)
    if request.method == 'GET':
        query = request.GET.get('q')

        ingredient_ids = search_ingredients(query=query)
        ingredients = [Ingredient.objects.get(id=i) for i in ingredient_ids]

        return render(request, 'cocktails/edit_cocktail_tags.html', {'recipe_part': recipe_part,
                                                                     'results': ingredients})
    else:
        return render(request, 'cocktails/edit_cocktail_tags.html', {'recipe_part': recipe_part})

def add_tag_to_recipe_part(request, recipe_part_id, ingredient_id):
    recipe_part = RecipePart.objects.get(pk=recipe_part_id)
    ingredient = Ingredient.objects.get(pk=ingredient_id)

    recipe_part.tagged_ingredients.add(ingredient)
    recipe_part.save()

    return redirect('editparttags', pk=recipe_part.pk)

def delete_tag_from_recipe_part(request, recipe_part_id, ingredient_id):
    recipe_part = RecipePart.objects.get(pk=recipe_part_id)
    ingredient = Ingredient.objects.get(pk=ingredient_id)

    recipe_part.tagged_ingredients.remove(ingredient)
    recipe_part.save()

    return redirect('editparttags', pk=recipe_part.pk)

def add_general_tag_to_recipe(request, recipe_pk, tag_pk):
    recipe = Recipe.objects.get(pk=recipe_pk)
    tag = RecipeTag.objects.get(pk=tag_pk)
    recipe.tags.add(tag)
    recipe.save()
    return redirect('viewcocktail', pk=recipe_pk)

def search_for_general_recipe_tags(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    if request.method == 'GET':
        query = request.GET.get('q')

        tags = RecipeTag.objects.all()

        return render(request, 'cocktails/search_general_tags.html', {'recipe': recipe,
                                                                     'results': tags})
    else:
        return render(request, 'cocktails/search_general_tags.html', {'recipe': recipe})

def define_new_tag(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    if request.method == 'POST':
        form = CreateRecipeTagForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            form_description = data['description']
            new_tag = RecipeTag(description=form_description)
            new_tag.save()

            recipe.tags.add(new_tag)
            recipe.save()

            return redirect('viewcocktail', pk=recipe.pk)
    else:
        form = CreateRecipeTagForm()
    return render(request, 'cocktails/define_new_recipe_tag.html', {'form': form,
                                                                    'recipe': recipe})
