"""
Forms for recipes app
"""
from django import forms
from .models import Recipe, Comment


class RecipeForm(forms.ModelForm):
    """
    Form for creating and updating recipes
    """
    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'ingredients', 'instructions',
            'prep_time', 'cook_time', 'servings', 'difficulty',
            'category', 'country', 'image', 'status'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Brief description of your recipe'}),
            'ingredients': forms.Textarea(attrs={'rows': 8, 'placeholder': 'List ingredients, one per line'}),
            'instructions': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Step-by-step instructions'}),
            'prep_time': forms.NumberInput(attrs={'placeholder': 'Minutes'}),
            'cook_time': forms.NumberInput(attrs={'placeholder': 'Minutes'}),
            'servings': forms.NumberInput(attrs={'placeholder': 'Number of servings'}),
        }
        labels = {
            'prep_time': 'Preparation Time (minutes)',
            'cook_time': 'Cooking Time (minutes)',
            'difficulty': 'Difficulty Level',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes for crispy forms
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class CommentForm(forms.ModelForm):
    """
    Form for adding comments to recipes
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Share your thoughts about this recipe...',
                'class': 'form-control'
            })
        }
        labels = {
            'content': 'Your Comment'
        }
