from django.contrib import admin
from .models import Category, Country, Recipe, Comment, Like


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model"""

    list_display = ("name", "slug", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")
    list_filter = ("created_at",)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """Admin interface for Country model"""

    list_display = ("name", "slug", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")
    list_filter = ("created_at",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Admin interface for Recipe model"""

    list_display = (
        "title",
        "author",
        "category",
        "country",
        "difficulty",
        "status",
        "created_at",
    )
    list_filter = ("status", "difficulty", "category", "country", "created_at")
    search_fields = ("title", "description", "ingredients", "author__username")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("status",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("title", "slug", "description", "author", "status")},
        ),
        (
            "Recipe Details",
            {
                "fields": (
                    "ingredients",
                    "instructions",
                    "prep_time",
                    "cook_time",
                    "servings",
                    "difficulty",
                )
            },
        ),
        ("Classification", {"fields": ("category", "country", "image")}),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for Comment model"""

    list_display = (
        "user", "recipe", "content_preview", "created_at", "approved"
    )
    list_filter = ("approved", "created_at")
    search_fields = ("user__username", "recipe__title", "content")
    list_editable = ("approved",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    def content_preview(self, obj):
        """Show preview of comment content"""
        return (
            obj.content[:50] + "..."
            if len(obj.content) > 50
            else obj.content
        )

    content_preview.short_description = "Content"


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """Admin interface for Like model"""

    list_display = ("user", "recipe", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "recipe__title")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
