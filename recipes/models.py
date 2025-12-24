from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    """
    Model representing a recipe category (e.g., Breakfast, Dinner, Dessert)
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_recipes", kwargs={"slug": self.slug})


class Country(models.Model):
    """
    Model representing a country/cuisine type (e.g., Italian, Mexican, Chinese)
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("country_recipes", kwargs={"slug": self.slug})


class Recipe(models.Model):
    """
    Model representing a recipe with all its details
    """

    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    # Basic Information
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(
        help_text="Brief description of the recipe"
    )
    ingredients = models.TextField(
        help_text="List all ingredients (one per line)"
    )
    instructions = models.TextField(
        help_text="Step-by-step cooking instructions"
    )

    # Time and Servings
    prep_time = models.PositiveIntegerField(
        help_text="Preparation time in minutes"
    )
    cook_time = models.PositiveIntegerField(
        help_text="Cooking time in minutes"
    )
    servings = models.PositiveIntegerField(
        default=4, help_text="Number of servings"
    )

    # Additional Details
    difficulty = models.CharField(
        max_length=10, choices=DIFFICULTY_CHOICES, default="medium"
    )
    image = models.ImageField(upload_to="recipes/", blank=True, null=True)

    # Relationships
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="recipes"
    )
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, related_name="recipes"
    )

    # Status and Timestamps
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="draft"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["status"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipe_detail", kwargs={"slug": self.slug})

    @property
    def total_time(self):
        """Calculate total cooking time"""
        return self.prep_time + self.cook_time

    def total_likes(self):
        """Return total number of likes"""
        return self.likes.count()

    def total_comments(self):
        """Return total number of approved comments"""
        return self.comments.filter(approved=True).count()


class Comment(models.Model):
    """
    Model representing a comment on a recipe
    """

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(
        default=True
    )  # Can be set to False for moderation

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"Comment by {self.user.username} on {self.recipe.title}"


class Like(models.Model):
    """
    Model representing a like/favorite on a recipe
    """

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="likes"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("recipe", "user")  # One like per user per recipe
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} likes {self.recipe.title}"
