from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cooking_time = models.PositiveIntegerField(help_text="Enter cooking time in minutes")
    difficulty = models.CharField(max_length=20, default="TBD")
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    pic = models.ImageField(upload_to="recipes", default="no_picture.jpeg")

    def calculate_difficulty(self):
        num_ingredients = self.ingredients.count()
        if self.cooking_time < 10 and num_ingredients < 4:
            return "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            return "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            return "Intermediate"
        else:
            return "Hard"

    def __str__(self):
        return self.title

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipes_recipe_ingredients'
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ingredient.name} in {self.recipe.title}"
