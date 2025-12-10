"""
Views for recipes app
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.http import JsonResponse
from .models import Recipe, Category, Country, Comment, Like
from .forms import RecipeForm, CommentForm


class RecipeListView(ListView):
    """
    Display list of all published recipes
    """
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 12
    
    def get_queryset(self):
        return Recipe.objects.filter(status='published').select_related(
            'author', 'category', 'country'
        ).annotate(
            like_count=Count('likes')
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['countries'] = Country.objects.all()
        
        # Get user's liked recipe IDs
        if self.request.user.is_authenticated:
            context['user_liked_ids'] = list(
                Like.objects.filter(user=self.request.user).values_list('recipe_id', flat=True)
            )
        else:
            context['user_liked_ids'] = []
        
        return context


class RecipeDetailView(DetailView):
    """
    Display detailed view of a single recipe
    """
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'
    
    def get_queryset(self):
        return Recipe.objects.select_related('author', 'category', 'country')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()
        context['comments'] = recipe.comments.filter(approved=True).select_related('user')
        context['comment_form'] = CommentForm()
        
        # Check if user has liked this recipe
        if self.request.user.is_authenticated:
            context['user_has_liked'] = Like.objects.filter(
                recipe=recipe, user=self.request.user
            ).exists()
        else:
            context['user_has_liked'] = False
            
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new recipe (requires login)
    """
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Recipe created successfully!')
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update an existing recipe. Only the recipe author or site admin can edit.
    """
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'
    
    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author or self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, 'Recipe updated successfully!')
        return super().form_valid(form)


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a recipe. Only the recipe author or site admin can delete.
    """
    model = Recipe
    template_name = 'recipes/recipe_confirm_delete.html'
    success_url = reverse_lazy('home')
    
    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author or self.request.user.is_staff
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Recipe deleted successfully!')
        return super().delete(request, *args, **kwargs)


class CategoryRecipeListView(ListView):
    """
    Display recipes filtered by category
    """
    model = Recipe
    template_name = 'recipes/category_recipes.html'
    context_object_name = 'recipes'
    paginate_by = 12
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Recipe.objects.filter(
            category=self.category, status='published'
        ).select_related('author', 'country').order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        
        # Get user's liked recipe IDs
        if self.request.user.is_authenticated:
            context['user_liked_ids'] = list(
                Like.objects.filter(user=self.request.user).values_list('recipe_id', flat=True)
            )
        else:
            context['user_liked_ids'] = []
        
        return context


class CountryRecipeListView(ListView):
    """
    Display recipes filtered by country/cuisine
    """
    model = Recipe
    template_name = 'recipes/country_recipes.html'
    context_object_name = 'recipes'
    paginate_by = 12
    
    def get_queryset(self):
        self.country = get_object_or_404(Country, slug=self.kwargs['slug'])
        return Recipe.objects.filter(
            country=self.country, status='published'
        ).select_related('author', 'category', 'country').order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['country'] = self.country
        context['categories'] = Category.objects.all()
        context['countries'] = Country.objects.all()
        
        # Get user's liked recipe IDs
        if self.request.user.is_authenticated:
            context['user_liked_ids'] = list(
                Like.objects.filter(user=self.request.user).values_list('recipe_id', flat=True)
            )
        else:
            context['user_liked_ids'] = []
        
        return context


class SearchRecipeView(ListView):
    """
    Search recipes by title or ingredients
    """
    model = Recipe
    template_name = 'recipes/search_results.html'
    context_object_name = 'recipes'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Recipe.objects.filter(
                Q(title__icontains=query) | 
                Q(ingredients__icontains=query) |
                Q(description__icontains=query),
                status='published'
            ).select_related('author', 'category', 'country').order_by('-created_at')
        return Recipe.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['categories'] = Category.objects.all()
        context['countries'] = Country.objects.all()
        
        # Get user's liked recipe IDs
        if self.request.user.is_authenticated:
            context['user_liked_ids'] = list(
                Like.objects.filter(user=self.request.user).values_list('recipe_id', flat=True)
            )
        else:
            context['user_liked_ids'] = []
        
        return context


class UserProfileView(ListView):
    """
    Display user's profile with their recipes
    """
    model = Recipe
    template_name = 'users/profile.html'
    context_object_name = 'recipes'
    paginate_by = 12
    
    def get_queryset(self):
        self.profile_user = get_object_or_404(User, username=self.kwargs['username'])
        return Recipe.objects.filter(
            author=self.profile_user, status='published'
        ).select_related('category', 'country').order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = self.profile_user
        context['total_recipes'] = self.get_queryset().count()
        
        # Get user's liked recipe IDs
        if self.request.user.is_authenticated:
            context['user_liked_ids'] = list(
                Like.objects.filter(user=self.request.user).values_list('recipe_id', flat=True)
            )
        else:
            context['user_liked_ids'] = []
        
        return context


class FavoritesListView(LoginRequiredMixin, ListView):
    """
    Display user's favorite/liked recipes
    """
    model = Recipe
    template_name = 'recipes/favorites.html'
    context_object_name = 'recipes'
    paginate_by = 12
    
    def get_queryset(self):
        # Get all recipes that the current user has liked
        liked_recipe_ids = Like.objects.filter(user=self.request.user).values_list('recipe_id', flat=True)
        return Recipe.objects.filter(
            id__in=liked_recipe_ids, status='published'
        ).select_related('author', 'category', 'country').annotate(
            like_count=Count('likes')
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_favorites'] = self.get_queryset().count()
        
        # Get user's liked recipe IDs (all recipes in favorites are liked by definition)
        context['user_liked_ids'] = list(
            Like.objects.filter(user=self.request.user).values_list('recipe_id', flat=True)
        )
        
        return context


@login_required
def add_comment(request, slug):
    """
    Add a comment to a recipe.
    
    Args:
        request (HttpRequest): The HTTP request object
        slug (str): The unique slug identifier for the recipe
    
    Returns:
        HttpResponseRedirect: Redirects to the recipe detail page
    
    Raises:
        Http404: If recipe with given slug does not exist
    """
    recipe = get_object_or_404(Recipe, slug=slug)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            try:
                comment = form.save(commit=False)
                comment.recipe = recipe
                comment.user = request.user
                comment.save()
                messages.success(request, 'Comment added successfully!')
            except Exception as e:
                messages.error(request, 'Unable to save comment. Please try again.')
        else:
            messages.error(request, 'Error adding comment. Please try again.')
    
    return redirect('recipe_detail', slug=slug)


@login_required
def delete_comment(request, pk):
    """
    Delete a comment. Only the comment author or site admin can delete.
    
    Args:
        request (HttpRequest): The HTTP request object
        pk (int): Primary key of the comment to delete
    
    Returns:
        HttpResponseRedirect: Redirects to the recipe detail page
    
    Raises:
        Http404: If comment with given pk does not exist
    """
    comment = get_object_or_404(Comment, pk=pk)
    
    if request.user == comment.user or request.user.is_staff:
        recipe_slug = comment.recipe.slug
        try:
            comment.delete()
            messages.success(request, 'Comment deleted successfully!')
        except Exception as e:
            messages.error(request, 'Unable to delete comment. Please try again.')
        return redirect('recipe_detail', slug=recipe_slug)
    else:
        messages.error(request, 'You can only delete your own comments.')
        return redirect('recipe_detail', slug=comment.recipe.slug)


@login_required
def toggle_like(request, slug):
    """
    Toggle like/unlike status on a recipe. Handles both AJAX and regular requests.
    
    Args:
        request (HttpRequest): The HTTP request object
        slug (str): The unique slug identifier for the recipe
    
    Returns:
        JsonResponse: If AJAX request, returns JSON with like status and count
        HttpResponseRedirect: If regular request, redirects to referring page or home
    
    Raises:
        Http404: If recipe with given slug does not exist
    """
    recipe = get_object_or_404(Recipe, slug=slug)
    
    try:
        like, created = Like.objects.get_or_create(recipe=recipe, user=request.user)
        
        if not created:
            like.delete()
            liked = False
            message = 'Recipe removed from favorites!'
        else:
            liked = True
            message = 'Recipe added to favorites!'
        
        # If AJAX request, return JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'liked': liked,
                'total_likes': recipe.total_likes()
            })
        
        # Otherwise, redirect back to the page the user came from
        messages.success(request, message)
        return redirect(request.META.get('HTTP_REFERER', 'home'))
        
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': 'Unable to update favorite status'
            }, status=500)
        else:
            messages.error(request, 'Unable to update favorite status. Please try again.')
            return redirect(request.META.get('HTTP_REFERER', 'home'))
