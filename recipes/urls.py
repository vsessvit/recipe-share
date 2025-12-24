"""
URL patterns for recipes app
"""

from django.urls import path
from . import views

urlpatterns = [
    # Home and recipe list
    path("", views.RecipeListView.as_view(), name="home"),
    path("recipes/", views.RecipeListView.as_view(), name="recipe_list"),
    # Recipe CRUD
    path(
        "recipe/create/",
        views.RecipeCreateView.as_view(),
        name="recipe_create"
    ),
    path(
        "recipe/<slug:slug>/",
        views.RecipeDetailView.as_view(),
        name="recipe_detail"
    ),
    path(
        "recipe/<slug:slug>/edit/",
        views.RecipeUpdateView.as_view(),
        name="recipe_update",
    ),
    path(
        "recipe/<slug:slug>/delete/",
        views.RecipeDeleteView.as_view(),
        name="recipe_delete",
    ),
    # Filter by category and country
    path(
        "category/<slug:slug>/",
        views.CategoryRecipeListView.as_view(),
        name="category_recipes",
    ),
    path(
        "cuisine/<slug:slug>/",
        views.CountryRecipeListView.as_view(),
        name="country_recipes",
    ),
    # Search
    path("search/", views.SearchRecipeView.as_view(), name="search_recipes"),
    # Comments
    path(
        "recipe/<slug:slug>/comment/",
        views.add_comment,
        name="add_comment"
    ),
    path(
        "comment/<int:pk>/delete/",
        views.delete_comment,
        name="delete_comment"
    ),
    # Likes
    path(
        "recipe/<slug:slug>/like/",
        views.toggle_like,
        name="toggle_like"
    ),
    path("favorites/", views.FavoritesListView.as_view(), name="favorites"),
    # User profile
    path(
        "profile/<str:username>/",
        views.UserProfileView.as_view(),
        name="user_profile"
    ),
]
