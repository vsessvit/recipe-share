"""
Comprehensive tests for users app
"""

from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import UserRegisterForm


class UserModelTest(TestCase):
    """Test User model functionality"""

    def test_user_creation(self):
        """Test user can be created"""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_user_str(self):
        """Test user string representation"""
        user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.assertEqual(str(user), "testuser")


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class RegistrationViewTest(TestCase):
    """Test user registration functionality"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()

    def test_registration_page_loads(self):
        """Test registration page loads correctly"""
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")
        self.assertContains(response, "Register")

    def test_registration_success(self):
        """Test user can register successfully"""
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "ComplexPass123!",
                "password2": "ComplexPass123!",
            },
        )
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.email, "newuser@example.com")
        self.assertRedirects(response, reverse("login"))

    def test_registration_password_mismatch(self):
        """Test registration fails with mismatched passwords"""
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "ComplexPass123!",
                "password2": "DifferentPass456!",
            },
        )
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        # Check that form has errors for password2
        self.assertFalse(response.context["form"].is_valid())
        self.assertIn("password2", response.context["form"].errors)

    def test_registration_duplicate_username(self):
        """Test registration fails with duplicate username"""
        User.objects.create_user(
            username="existinguser",
            password="testpass123"
        )
        response = self.client.post(
            reverse("register"),
            {
                "username": "existinguser",
                "email": "new@example.com",
                "password1": "ComplexPass123!",
                "password2": "ComplexPass123!",
            },
        )
        self.assertEqual(User.objects.count(), 1)
        self.assertFalse(response.context["form"].is_valid())
        self.assertIn("username", response.context["form"].errors)


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class LoginViewTest(TestCase):
    """Test user login functionality"""

    def setUp(self):
        """Set up test client and user"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    def test_login_page_loads(self):
        """Test login page loads correctly"""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    def test_login_success(self):
        """Test user can login successfully"""
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "testpass123"
            }
        )
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_invalid_credentials(self):
        """Test login fails with invalid credentials"""
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "wrongpassword"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_login_inactive_user(self):
        """Test inactive user cannot login"""
        self.user.is_active = False
        self.user.save()
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "testpass123"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


@override_settings(
    STATICFILES_STORAGE="django.contrib.staticfiles.storage.StaticFilesStorage"
)
class LogoutViewTest(TestCase):
    """Test user logout functionality"""

    def setUp(self):
        """Set up test client and user"""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    def test_logout_success(self):
        """Test user can logout successfully"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)


class UserRegisterFormTest(TestCase):
    """Test UserRegisterForm"""

    def test_form_valid_data(self):
        """Test form is valid with correct data"""
        form = UserRegisterForm(
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password1": "ComplexPass123!",
                "password2": "ComplexPass123!",
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_missing_email(self):
        """Test form is invalid without email"""
        form = UserRegisterForm(
            data={
                "username": "testuser",
                "password1": "ComplexPass123!",
                "password2": "ComplexPass123!",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_form_password_mismatch(self):
        """Test form is invalid with mismatched passwords"""
        form = UserRegisterForm(
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password1": "ComplexPass123!",
                "password2": "DifferentPass456!",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_form_saves_user(self):
        """Test form saves user correctly"""
        form = UserRegisterForm(
            data={
                "username": "testuser",
                "email": "test@example.com",
                "password1": "ComplexPass123!",
                "password2": "ComplexPass123!",
            }
        )
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("ComplexPass123!"))


class UserUpdateFormTest(TestCase):
    """Test User Update Form (profile updates)"""

    def setUp(self):
        """Set up test user"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )

    def test_user_can_be_updated(self):
        """Test user fields can be updated"""
        self.user.username = "updateduser"
        self.user.email = "updated@example.com"
        self.user.save()
        updated_user = User.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.username, "updateduser")
        self.assertEqual(updated_user.email, "updated@example.com")
