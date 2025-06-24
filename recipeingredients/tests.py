from django.test import TestCase
from recipes.models import Recipe
from ingredients.models import Ingredient
from .models import RecipeIngredient
from django.core.exceptions import ValidationError


class TestRecipeIngredientModel(TestCase):
    def setUp(self):
        # Setup recipes and ingredients
        self.ingredient1 = Ingredient.objects.create(name="Salt")
        self.ingredient2 = Ingredient.objects.create(name="Pepper")

        self.recipe1 = Recipe.objects.create(
            title="Dish 1",
            description="Test dish 1",
            cooking_time=10,
            pic="pic1.jpg"
        )
        self.recipe2 = Recipe.objects.create(
            title="Dish 2",
            description="Test dish 2",
            cooking_time=15,
            pic="pic2.jpg"
        )
        # Link some ingredients
        self.rel1 = RecipeIngredient.objects.create(recipe=self.recipe1, ingredient=self.ingredient1)
        self.rel2 = RecipeIngredient.objects.create(recipe=self.recipe1, ingredient=self.ingredient2)
        self.rel3 = RecipeIngredient.objects.create(recipe=self.recipe2, ingredient=self.ingredient2)

    def test_str_method(self):
        self.assertEqual(str(self.rel1), "Salt - Dish 1")
        self.assertEqual(str(self.rel3), "Pepper - Dish 2")

    def test_cascade_delete_recipe(self):
        self.recipe1.delete()
        # RecipeIngredient related to recipe1 should be deleted
        self.assertFalse(RecipeIngredient.objects.filter(id=self.rel1.id).exists())
        self.assertFalse(RecipeIngredient.objects.filter(id=self.rel2.id).exists())
        # But rel3 related to recipe2 still exists
        self.assertTrue(RecipeIngredient.objects.filter(id=self.rel3.id).exists())

    def test_cascade_delete_ingredient(self):
        self.ingredient2.delete()
        # RecipeIngredients related to ingredient2 should be deleted
        self.assertFalse(RecipeIngredient.objects.filter(id=self.rel2.id).exists())
        self.assertFalse(RecipeIngredient.objects.filter(id=self.rel3.id).exists())
        # rel1 related to ingredient1 still exists
        self.assertTrue(RecipeIngredient.objects.filter(id=self.rel1.id).exists())

    def test_recipe_multiple_ingredients(self):
        # Recipe1 should have 2 ingredients linked
        self.assertEqual(self.recipe1.recipe_ingredients.count(), 2)

    def test_ingredient_multiple_recipes(self):
        # Ingredient2 should be linked to 2 recipes
        count = RecipeIngredient.objects.filter(ingredient=self.ingredient2).count()
        self.assertEqual(count, 2)

    def test_invalid_recipeingredient_creation(self):
        recipeingredient = RecipeIngredient(recipe=None, ingredient=self.ingredient1)
        with self.assertRaises(ValidationError):
            recipeingredient.full_clean()  # This triggers validation errors before save
            recipeingredient.save()
