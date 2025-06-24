from django.db import models
from recipes.models import Recipe
from ingredients.models import Ingredient

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients'  # e.g. use this
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.ingredient} - {self.recipe}"
