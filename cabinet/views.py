from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .search_utils import search_ingredients
from core.models import Ingredient

# Create your views here.

@login_required
def view_cabinet(request):
    user = request.user
    return render(request, 'cabinet/view_cabinet.html', {'cabinet': user.cabinet})

@login_required()
def search_for_cabinet(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        ingredient_ids = search_ingredients(query=query)
        ingredients = [Ingredient.objects.get(id=i) for i in ingredient_ids]

        return render(request, 'cabinet/search_for_cabinet.html', {'results': ingredients})

    else:
        return render(request, 'cabinet/search_for_cabinet.html', {})

@login_required
def add_to_cabinet(request, pk):
    cabinet = request.user.cabinet
    ingredient = Ingredient.objects.get(pk=pk)
    cabinet.add(ingredient)

    request.user.save()

    return redirect('cabinet')

@login_required
def delete_from_cabinet(request, pk):
    cabinet = request.user.cabinet
    ingredient = Ingredient.objects.get(pk=pk)
    cabinet.remove(ingredient)

    request.user.save()

    return redirect('cabinet')

