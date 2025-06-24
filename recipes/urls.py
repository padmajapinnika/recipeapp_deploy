from django.urls import path
from . import views 
from .views import home, recipe_list, recipe_detail, recipe_search, login_view, logout_view,signup_view

app_name = 'recipes'

urlpatterns = [
    path('', home, name='home'), 
    path('signup/', views.signup_view, name='signup'), 
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('list/', recipe_list, name='recipe_list'),
    path('detail/<int:pk>/', recipe_detail, name='recipe_detail'),
    path('search/', recipe_search, name='recipe_search'),
    path('add/', views.add_recipe_view, name='add_recipe'),
    path('about/', views.about_me_view, name='about_me'),

]
