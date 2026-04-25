import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.template.context_processors import request

from .models import Recipe
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm
from django.contrib import messages


from accounts.models import CustomUser
from recipes.forms import RecipeForm
from recipes.models import Recipe
from django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator



def recipe_list(request):
    recipes = Recipe.objects.all().order_by("-pk").select_related('user')

    paginator = Paginator(recipes, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        # "user": request.user,
    }
    return render(request, "recipes/home.html", context)

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

@login_required
def create_recipe(request: HttpRequest):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            # aici se intampla salvarea in baza de date
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.author = request.user.username
            recipe.save()
            messages.success(request, f'Reteta "{recipe.title}" a fost adaugata cu succes!')
            return redirect("recipe_list")
    else:
        form = RecipeForm()

    context = {
        'form': form
    }
    return render(request, "recipes/recipe_form.html", context)

def delete_recipe(request: HttpRequest, pk: int):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == "POST":
        recipe.delete()
        return redirect("recipe_list")
    else:
        return render(request, "recipes/recipe_confirm_delete.html", { "recipe": recipe })

def delete_recipe_image(request: HttpRequest, pk: int):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == "POST":
        if recipe.image is not None:
            if os.path.isfile(recipe.image.path):
                os.remove(recipe.image.path)
                recipe.image = None
                recipe.save()

        return redirect("recipe_list")


def update_recipe(request: HttpRequest, pk: int):
    # cartea care exista deja din baza de date
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == "POST":
        # request.POST = { "title": "Harry Potter1", "author": "Rowling" }
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect("recipe_list")
    else:
        form = RecipeForm(instance=recipe)

    return render(request, "recipes/recipe_form.html", {"form": form})

def check_recipe_count(request: HttpRequest):
    count = Recipe.objects.count()
    return render(request, "recipes/recipe_count.html", {"recipe_count": count})

def user_recipes(request: HttpRequest, pk: int):
    # pk -> id-ul user-ului
    user = get_object_or_404(CustomUser, pk=pk)
    recipes = user.recipes.all().order_by("-pk")

    paginator = Paginator(recipes, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj
    }

    return render(request, "recipes/home.html", context)

def search_recipes(request: HttpRequest):
    q = request.GET.get("q")
    author = request.GET.get("author")
    sort = request.GET.get("sort", "newest")

    recipes = Recipe.objects.all()

    if q:
        recipes = recipes.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q)
        )
    if author:
        recipes = recipes.filter(user__username__icontains=author)
    if sort == "oldest":
        recipes = recipes.order_by("pk")
    else:
        recipes = recipes.order_by("-pk")

    paginator = Paginator(recipes, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj
    }

    return render(request, "recipes/home.html", context)

    # if q is None:
    #     recipes = Recipe.objects.all().order_by("-pk")
    # else:
    #     recipes = Recipe.objects.filter(title__contains=q).all().order_by("-pk")
    #
    # paginator = Paginator(recipes, 5)
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)
    #
    # context = {
    #     "page_obj": page_obj
    # }
    #
    # return render(request, "recipes/home.html", context)
    # return render(request, "recipes/home.html", context)


def simple_endpoint(request: HttpRequest):
    return HttpResponse("{ 'content': 'Hello this is my response to your request'}", status=202)

