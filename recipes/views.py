from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from .forms import RecipeSearchForm
from .models import Recipe
import pandas as pd
from .utils import get_chart
from .forms import SignUpForm
from .forms import RecipeForm
from recipes.models import Recipe
from ingredients.models import Ingredient
from recipeingredients.models import RecipeIngredient
from django.contrib import messages


@login_required(login_url='recipes:login')
def add_recipe_view(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user  # if you have a user field
            recipe.save()
            return redirect('recipes:recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_add.html', {'form': form})


@login_required(login_url='recipes:login')
def home(request):
    return render(request, 'recipes/recipes_home.html')

@login_required(login_url='recipes:login')
def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

@login_required(login_url='recipes:login')
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

@login_required(login_url='recipes:login')
def recipe_search(request):
    form = RecipeSearchForm(request.GET or None)
    chart = None
    recipes = Recipe.objects.none()

    if form.is_valid():
        query = form.cleaned_data.get('query')  # Search text
        chart_type = form.cleaned_data.get('chart_type')

        if query:
            recipes = Recipe.objects.filter(
                Q(title__icontains=query) |
                Q(recipe_ingredients__ingredient__name__icontains=query)
            ).distinct()
        else:
            recipes = Recipe.objects.all()

        # Generate chart if requested and recipes exist
        if chart_type and recipes.exists():
            df = pd.DataFrame(recipes.values('id', 'title', 'cooking_time', 'difficulty'))
            chart = get_chart(chart_type, df)

    context = {
        'form': form,
        'recipes': recipes,
        'chart': chart,
    }
    return render(request, 'recipes/recipe_list.html', context)

def login_view(request):
    error_message = None
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('recipes:home')
        else:
            error_message = 'Oops... something went wrong'
    context = {
        'form': form,
        'error_message': error_message
    }
    return render(request, 'auth/home.html', context)

def logout_view(request):
    logout(request)
    return redirect('recipes:login')

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user immediately after signup
            return redirect('recipes:home')  # Redirect to home or any page you want
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', {'form': form})




@login_required
def add_recipe_view(request):
    if request.method == 'POST':
        print("Form submitted!")  # DEBUG
        form = RecipeForm(request.POST, request.FILES)
        # Set the queryset here to include all valid ingredients
        form.fields['ingredients'].queryset = Ingredient.objects.all()

        selected_ingredient_ids = request.POST.getlist('ingredients')

        if form.is_valid():
            print("Form is valid!")  # DEBUG
            recipe = form.save(commit=False)
            recipe.user = request.user  # if you have user field
            recipe.save()

            # Optionally clear old relations if any
            RecipeIngredient.objects.filter(recipe=recipe).delete()

            for ingredient_id in selected_ingredient_ids:
                try:
                    ingredient = Ingredient.objects.get(id=ingredient_id)
                    RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient)
                except Ingredient.DoesNotExist:
                    print(f"Ingredient with ID {ingredient_id} not found.")

            recipe.difficulty = recipe.calculate_difficulty()
            recipe.save(update_fields=['difficulty'])

            messages.success(request, "🎉 Recipe added successfully!")
            return redirect('recipes:recipe_list')
        else:
            print("Form is invalid:", form.errors)
            messages.error(request, "Form submission failed. Please check the errors.")
    else:
        form = RecipeForm()
        form.fields['ingredients'].queryset = Ingredient.objects.all()

    all_ingredients = Ingredient.objects.all()
    return render(request, 'recipes/recipe_add.html', {
        'form': form,
        'ingredients': all_ingredients
    })

def about_me_view(request):
    return render(request, 'recipes/about_me.html')