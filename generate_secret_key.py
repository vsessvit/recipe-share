#!/usr/bin/env python
"""
Generate a new Django SECRET_KEY
Run this to generate a secure secret key for production
"""
from django.core.management.utils import get_random_secret_key

if __name__ == '__main__':
    print("Generated SECRET_KEY:")
    print(get_random_secret_key())
    print("\nUse this for your Heroku config:")
    print("heroku config:set SECRET_KEY=\"" + get_random_secret_key() + "\"")
