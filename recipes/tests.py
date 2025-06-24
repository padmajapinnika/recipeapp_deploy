from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Recipe, Ingredient, RecipeIngredient

class TestRecipeModel(TestCase):
    def setUp(self):
        # Create and log in a test user
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

        # Create Ingredients
        self.ingredient1 = Ingredient.objects.create(name="Salt")
        self.ingredient2 = Ingredient.objects.create(name="Pepper")

        # Create a Recipe
        self.recipe = Recipe.objects.create(
            title="Simple Dish",
            description="Just a test recipe.",
            cooking_time=5,
            pic="test_pic.jpg"
        )
        # Link Ingredients to Recipe
        RecipeIngredient.objects.create(recipe=self.recipe, ingredient=self.ingredient1)
        RecipeIngredient.objects.create(recipe=self.recipe, ingredient=self.ingredient2)

    def test_recipe_str(self):
        self.assertEqual(str(self.recipe), "Simple Dish")

    def test_ingredient_str(self):
        self.assertEqual(str(self.ingredient1), "Salt")

    def test_recipe_ingredient_str(self):
        relation = RecipeIngredient.objects.get(recipe=self.recipe, ingredient=self.ingredient1)
        self.assertEqual(str(relation), "Salt in Simple Dish")

    def test_calculate_difficulty_easy(self):
        self.assertEqual(self.recipe.calculate_difficulty(), "Easy")

    def test_recipe_has_correct_ingredients(self):
        self.assertEqual(self.recipe.ingredients.count(), 2)

    def test_recipe_list_view(self):
        response = self.client.get(reverse('recipes:recipe_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Simple Dish")

    def test_recipe_detail_view(self):
        response = self.client.get(reverse('recipes:recipe_detail', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Just a test recipe.")

    def test_home_view(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    

    def test_recipe_search_view(self):
        response = self.client.get(reverse('recipes:recipe_search') + '?query=Simple')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Simple Dish')

        # Test with no matching results
        response = self.client.get(reverse('recipes:recipe_search') + '?query=Nonexistent')
        self.assertContains(response, 'No recipes found.')

    def test_redirect_if_not_logged_in(self):
        self.client.logout()  # Logout to simulate anonymous user

        response = self.client.get(reverse('recipes:recipe_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

        response = self.client.get(reverse('recipes:recipe_detail', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_ingredient_name_cannot_be_empty(self):
        ingredient = Ingredient(name='')
        with self.assertRaises(ValidationError):
            ingredient.full_clean()  # Validate before save
            ingredient.save()

    def test_removing_ingredient_removes_relation(self):
        self.ingredient1.delete()
        self.assertFalse(RecipeIngredient.objects.filter(ingredient=self.ingredient1).exists())
