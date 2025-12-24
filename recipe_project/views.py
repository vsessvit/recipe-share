"""
Custom error views for recipe_project.
"""

from django.shortcuts import render


def custom_404(request, exception):
    """
    Custom 404 error handler.

    Args:
        request: The HTTP request object
        exception: The exception that triggered the 404

    Returns:
        HttpResponse: Rendered 404 template with 404 status code
    """
    return render(request, '404.html', status=404)


def custom_500(request):
    """
    Custom 500 error handler.

    Args:
        request: The HTTP request object

    Returns:
        HttpResponse: Rendered 500 template with 500 status code
    """
    return render(request, '500.html', status=500)
