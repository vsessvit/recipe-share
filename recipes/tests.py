"""
Comprehensive tests for recipes app
"""
from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Recipe, Category, Country, Comment, Like


class RecipeModelTest(TestCase):
    """Test Recipe model functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.country = Country.objects.create(
            name='Test Country',
            slug='test-country'
        )
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            slug='test-recipe',
            description='Test description',
            ingredients='Test ingredients',
            instructions='Test instructions',
            prep_time=10,
            cook_time=20,
            servings=4,
            difficulty='easy',
            status='published',
            author=self.user,
            category=self.category,
            country=self.country
        )
    
    def test_recipe_creation(self):
        """Test recipe is created correctly"""
        self.assertEqual(self.recipe.title, 'Test Recipe')
        self.assertEqual(self.recipe.author, self.user)
        self.assertEqual(self.recipe.total_time, 30)
        self.assertEqual(self.recipe.status, 'published')
    
    def test_recipe_str(self):
        """Test recipe string representation"""
        self.assertEqual(str(self.recipe), 'Test Recipe')
    
    def test_recipe_absolute_url(self):
        """Test recipe get_absolute_url method"""
        self.assertEqual(
            self.recipe.get_absolute_url(),
            reverse('recipe_detail', kwargs={'slug': 'test-recipe'})
        )
    
    def test_recipe_total_time(self):
        """Test total time calculation"""
        self.assertEqual(self.recipe.total_time, 30)
    
    def test_total_likes(self):
        """Test total likes count"""
        Like.objects.create(recipe=self.recipe, user=self.user)
        self.assertEqual(self.recipe.total_likes(), 1)
    
    def test_total_comments(self):
        """Test total approved comments count"""
        Comment.objects.create(
            recipe=self.recipe,
            user=self.user,
            content='Great recipe!',
            approved=True
        )
        Comment.objects.create(
            recipe=self.recipe,
            user=self.user,
            content='Not approved',
            approved=False
        )
        self.assertEqual(self.recipe.total_comments(), 1)


class CategoryModelTest(TestCase):
    """Test Category model functionality"""
    
    def test_category_creation(self):
        """Test category creation with auto slug"""
        category = Category.objects.create(name='Breakfast')
        self.assertEqual(str(category), 'Breakfast')
        self.assertEqual(category.slug, 'breakfast')
    
    def test_category_absolute_url(self):
        """Test category get_absolute_url"""
        category = Category.objects.create(name='Dinner')
        self.assertEqual(
            category.get_absolute_url(),
            reverse('category_recipes', kwargs={'slug': 'dinner'})
        )


class CountryModelTest(TestCase):
    """Test Country model functionality"""
    
    def test_country_creation(self):
        """Test country creation with auto slug"""
        country = Country.objects.create(name='Italian')
        self.assertEqual(str(country), 'Italian')
        self.assertEqual(country.slug, 'italian')
    
    def test_country_absolute_url(self):
        """Test country get_absolute_url"""
        country = Country.objects.create(name='Mexican')
        self.assertEqual(
            country.get_absolute_url(),
            reverse('country_recipes', kwargs={'slug': 'mexican'})
        )


class CommentModelTest(TestCase):
    """Test Comment model functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Dinner')
        self.country = Country.objects.create(name='Italian')
        self.recipe = Recipe.objects.create(
            title='Pasta',
            description='Delicious pasta',
            ingredients='Pasta, sauce',
            instructions='Cook pasta',
            prep_time=5,
            cook_time=10,
            servings=2,
            author=self.user,
            category=self.category,
            country=self.country,
            status='published'
        )
    
    def test_comment_creation(self):
        """Test comment is created successfully"""
        comment = Comment.objects.create(
            recipe=self.recipe,
            user=self.user,
            content='Great recipe!'
        )
        self.assertEqual(comment.recipe, self.recipe)
        self.assertEqual(comment.user, self.user)
        self.assertTrue(comment.approved)
        self.assertEqual(str(comment), 'Comment by testuser on Pasta')


class LikeModelTest(TestCase):
    """Test Like model functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Dinner')
        self.country = Country.objects.create(name='Italian')
        self.recipe = Recipe.objects.create(
            title='Pasta',
            description='Delicious pasta',
            ingredients='Pasta, sauce',
            instructions='Cook pasta',
            prep_time=5,
            cook_time=10,
            servings=2,
            author=self.user,
            category=self.category,
            country=self.country,
            status='published'
        )
    
    def test_like_creation(self):
        """Test like is created successfully"""
        like = Like.objects.create(recipe=self.recipe, user=self.user)
        self.assertEqual(like.recipe, self.recipe)
        self.assertEqual(like.user, self.user)
        self.assertEqual(str(like), 'testuser likes Pasta')
    
    def test_like_unique_together(self):
        """Test one user can only like a recipe once"""
        Like.objects.create(recipe=self.recipe, user=self.user)
        with self.assertRaises(Exception):
            Like.objects.create(recipe=self.recipe, user=self.user)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class RecipeViewTest(TestCase):
    """Test Recipe views"""
    
    def setUp(self):
        """Set up test data and client"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.admin = User.objects.create_user(
            username='admin',
            password='admin123',
            is_staff=True
        )
        self.category = Category.objects.create(name='Dinner')
        self.country = Country.objects.create(name='Italian')
        self.recipe = Recipe.objects.create(
            title='Pasta Carbonara',
            description='Delicious pasta',
            ingredients='Pasta, eggs, bacon',
            instructions='Cook pasta, mix with eggs',
            prep_time=5,
            cook_time=10,
            servings=2,
            author=self.user,
            category=self.category,
            country=self.country,
            status='published'
        )
    
    def test_recipe_list_view(self):
        """Test recipe list page loads correctly"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pasta Carbonara')
        self.assertTemplateUsed(response, 'recipes/recipe_list.html')
    
    def test_recipe_detail_view(self):
        """Test recipe detail page loads correctly"""
        response = self.client.get(
            reverse('recipe_detail', kwargs={'slug': self.recipe.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pasta Carbonara')
        self.assertContains(response, 'Delicious pasta')
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')
    
    def test_recipe_create_requires_login(self):
        """Test creating recipe requires authentication"""
        response = self.client.get(reverse('recipe_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/recipe/create/')
    
    def test_recipe_create_authenticated(self):
        """Test authenticated user can access create page"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('recipe_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_form.html')
    
    def test_recipe_create_post(self):
        """Test creating a recipe via POST"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('recipe_create'), {
            'title': 'New Recipe',
            'description': 'Test description',
            'ingredients': 'Test ingredients',
            'instructions': 'Test instructions',
            'prep_time': 10,
            'cook_time': 20,
            'servings': 4,
            'difficulty': 'easy',
            'category': self.category.id,
            'country': self.country.id,
            'status': 'published'
        })
        self.assertEqual(Recipe.objects.count(), 2)
        new_recipe = Recipe.objects.get(title='New Recipe')
        self.assertEqual(new_recipe.author, self.user)
    
    def test_recipe_update_only_author(self):
        """Test only author can update recipe"""
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(
            reverse('recipe_update', kwargs={'slug': self.recipe.slug})
        )
        self.assertEqual(response.status_code, 403)
    
    def test_recipe_update_author_can_edit(self):
        """Test author can edit their recipe"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('recipe_update', kwargs={'slug': self.recipe.slug})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_update_admin_can_edit(self):
        """Test admin can edit any recipe"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(
            reverse('recipe_update', kwargs={'slug': self.recipe.slug})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_delete_only_author(self):
        """Test only author can delete recipe"""
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(
            reverse('recipe_delete', kwargs={'slug': self.recipe.slug})
        )
        self.assertEqual(response.status_code, 403)
    
    def test_recipe_delete_admin_can_delete(self):
        """Test admin can delete any recipe"""
        self.client.login(username='admin', password='admin123')
        response = self.client.post(
            reverse('recipe_delete', kwargs={'slug': self.recipe.slug})
        )
        self.assertEqual(Recipe.objects.count(), 0)
    
    def test_category_filter_view(self):
        """Test filtering recipes by category"""
        response = self.client.get(
            reverse('category_recipes', kwargs={'slug': self.category.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pasta Carbonara')
    
    def test_country_filter_view(self):
        """Test filtering recipes by country"""
        response = self.client.get(
            reverse('country_recipes', kwargs={'slug': self.country.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pasta Carbonara')
    
    def test_search_view(self):
        """Test search functionality"""
        response = self.client.get(reverse('search_recipes'), {'q': 'pasta'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pasta Carbonara')
    
    def test_search_view_no_results(self):
        """Test search with no results"""
        response = self.client.get(reverse('search_recipes'), {'q': 'nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Pasta Carbonara')

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class CommentViewTest(TestCase):
    """Test Comment functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.admin = User.objects.create_user(
            username='admin',
            password='admin123',
            is_staff=True
        )
        self.category = Category.objects.create(name='Dinner')
        self.country = Country.objects.create(name='Italian')
        self.recipe = Recipe.objects.create(
            title='Pasta',
            description='Test',
            ingredients='Test',
            instructions='Test',
            prep_time=5,
            cook_time=10,
            servings=2,
            author=self.user,
            category=self.category,
            country=self.country,
            status='published'
        )
    
    def test_add_comment_requires_login(self):
        """Test adding comment requires authentication"""
        response = self.client.post(
            reverse('add_comment', kwargs={'slug': self.recipe.slug}),
            {'content': 'Test comment'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_add_comment_authenticated(self):
        """Test authenticated user can add comment"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('add_comment', kwargs={'slug': self.recipe.slug}),
            {'content': 'Great recipe!'}
        )
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.content, 'Great recipe!')
        self.assertEqual(comment.user, self.user)
    
    def test_delete_comment_only_author(self):
        """Test only comment author can delete"""
        comment = Comment.objects.create(
            recipe=self.recipe,
            user=self.user,
            content='Test comment'
        )
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.post(
            reverse('delete_comment', kwargs={'pk': comment.pk})
        )
        self.assertEqual(Comment.objects.count(), 1)
    
    def test_delete_comment_admin_can_delete(self):
        """Test admin can delete any comment"""
        comment = Comment.objects.create(
            recipe=self.recipe,
            user=self.user,
            content='Test comment'
        )
        self.client.login(username='admin', password='admin123')
        response = self.client.post(
            reverse('delete_comment', kwargs={'pk': comment.pk})
        )
        self.assertEqual(Comment.objects.count(), 0)

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class LikeViewTest(TestCase):
    """Test Like/Unlike functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Dinner')
        self.country = Country.objects.create(name='Italian')
        self.recipe = Recipe.objects.create(
            title='Pasta',
            description='Test',
            ingredients='Test',
            instructions='Test',
            prep_time=5,
            cook_time=10,
            servings=2,
            author=self.user,
            category=self.category,
            country=self.country,
            status='published'
        )
    
    def test_toggle_like_requires_login(self):
        """Test liking requires authentication"""
        response = self.client.post(
            reverse('toggle_like', kwargs={'slug': self.recipe.slug})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
    
    def test_toggle_like_create(self):
        """Test creating a like"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('toggle_like', kwargs={'slug': self.recipe.slug})
        )
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(self.recipe.total_likes(), 1)
    
    def test_toggle_like_remove(self):
        """Test removing a like"""
        Like.objects.create(recipe=self.recipe, user=self.user)
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('toggle_like', kwargs={'slug': self.recipe.slug})
        )
        self.assertEqual(Like.objects.count(), 0)
        self.assertEqual(self.recipe.total_likes(), 0)
    
    def test_favorites_view_requires_login(self):
        """Test favorites page requires authentication"""
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 302)
    
    def test_favorites_view_shows_liked_recipes(self):
        """Test favorites page shows user's liked recipes"""
        Like.objects.create(recipe=self.recipe, user=self.user)
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pasta')

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class UserProfileViewTest(TestCase):
    """Test User Profile functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Dinner')
        self.country = Country.objects.create(name='Italian')
        self.recipe = Recipe.objects.create(
            title='Pasta',
            description='Test',
            ingredients='Test',
            instructions='Test',
            prep_time=5,
            cook_time=10,
            servings=2,
            author=self.user,
            category=self.category,
            country=self.country,
            status='published'
        )
    
    def test_user_profile_view(self):
        """Test user profile page loads correctly"""
        response = self.client.get(
            reverse('user_profile', kwargs={'username': 'testuser'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'Pasta')
