"""Template tags for image optimization"""
from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def cloudinary_thumb(image_url, width=400, height=300):
    """
    Generate optimized Cloudinary thumbnail URL
    
    Args:
        image_url: Original Cloudinary image URL
        width: Target width in pixels
        height: Target height in pixels
    
    Returns:
        Optimized image URL with transformations
    """
    if not image_url or 'res.cloudinary.com' not in str(image_url):
        return image_url
    
    # Insert Cloudinary transformations
    # Format: w_400,h_300,c_fill,f_auto,q_auto
    transformation = f"w_{width},h_{height},c_fill,f_auto,q_auto:good"
    
    # Find upload position and insert transformation
    url_str = str(image_url)
    if '/upload/' in url_str:
        optimized = url_str.replace('/upload/', f'/upload/{transformation}/')
        return optimized
    
    return image_url


@register.simple_tag
def cloudinary_hero(image_url, width=1200, height=600):
    """
    Generate optimized Cloudinary hero/detail image URL
    
    Args:
        image_url: Original Cloudinary image URL
        width: Target width in pixels
        height: Target height in pixels
    
    Returns:
        Optimized image URL with transformations
    """
    if not image_url or 'res.cloudinary.com' not in str(image_url):
        return image_url
    
    transformation = f"w_{width},h_{height},c_limit,f_auto,q_auto:good"
    
    url_str = str(image_url)
    if '/upload/' in url_str:
        optimized = url_str.replace('/upload/', f'/upload/{transformation}/')
        return optimized
    
    return image_url
