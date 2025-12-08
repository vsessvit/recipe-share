from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes.models import Category, Country, Recipe
from django.utils.text import slugify
import os
from django.core.files import File
from urllib.request import urlretrieve
from pathlib import Path


class Command(BaseCommand):
    help = 'Populate database with sample recipes'

    def handle(self, *args, **kwargs):
        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True}
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user'))

        # Sample recipes data
        recipes_data = [
            {
                'title': 'Classic Spaghetti Carbonara',
                'category': 'Dinner',
                'country': 'Italian',
                'description': 'A traditional Italian pasta dish made with eggs, cheese, pancetta, and black pepper.',
                'ingredients': '''400g spaghetti
200g pancetta or guanciale, diced
4 large eggs
100g Pecorino Romano cheese, grated
Black pepper to taste
Salt for pasta water''',
                'instructions': '''1. Bring a large pot of salted water to boil and cook spaghetti according to package directions.
2. While pasta cooks, fry pancetta in a large skillet until crispy.
3. In a bowl, whisk together eggs and grated cheese.
4. Drain pasta, reserving 1 cup of pasta water.
5. Add hot pasta to the pancetta, remove from heat.
6. Quickly stir in egg mixture, adding pasta water as needed for creamy consistency.
7. Season with black pepper and serve immediately.''',
                'prep_time': 10,
                'cook_time': 20,
                'servings': 4,
                'difficulty': 'medium',
                'status': 'published'
            },
            {
                'title': 'Chicken Tikka Masala',
                'category': 'Dinner',
                'country': 'Indian',
                'description': 'Tender chicken pieces in a creamy, spiced tomato sauce - a beloved Indian classic.',
                'ingredients': '''600g chicken breast, cubed
200g plain yogurt
3 tbsp tikka masala paste
2 onions, diced
4 cloves garlic, minced
400g canned tomatoes
200ml heavy cream
2 tbsp vegetable oil
Fresh cilantro for garnish
Rice for serving''',
                'instructions': '''1. Marinate chicken in yogurt and 2 tbsp tikka masala paste for at least 1 hour.
2. Heat oil in a large pan and cook chicken until browned. Set aside.
3. Sauté onions and garlic until softened.
4. Add remaining tikka masala paste and cook for 1 minute.
5. Add canned tomatoes and simmer for 10 minutes.
6. Stir in cream and cooked chicken.
7. Simmer for 10 more minutes until chicken is cooked through.
8. Garnish with cilantro and serve with rice.''',
                'prep_time': 75,
                'cook_time': 30,
                'servings': 6,
                'difficulty': 'medium',
                'status': 'published'
            },
            {
                'title': 'Beef Tacos',
                'category': 'Lunch',
                'country': 'Mexican',
                'description': 'Flavorful seasoned beef in crispy or soft tortillas with fresh toppings.',
                'ingredients': '''500g ground beef
1 onion, diced
2 cloves garlic, minced
2 tbsp taco seasoning
8 taco shells or tortillas
Shredded lettuce
Diced tomatoes
Shredded cheese
Sour cream
Salsa''',
                'instructions': '''1. Brown ground beef with onion and garlic in a large skillet.
2. Drain excess fat.
3. Add taco seasoning and 1/4 cup water.
4. Simmer until water is absorbed.
5. Warm taco shells according to package directions.
6. Fill shells with beef mixture.
7. Top with lettuce, tomatoes, cheese, sour cream, and salsa.''',
                'prep_time': 10,
                'cook_time': 15,
                'servings': 4,
                'difficulty': 'easy',
                'status': 'published'
            },
            {
                'title': 'Kung Pao Chicken',
                'category': 'Dinner',
                'country': 'Chinese',
                'description': 'A spicy Sichuan dish with chicken, peanuts, and vegetables in savory sauce.',
                'ingredients': '''500g chicken breast, cubed
100g roasted peanuts
2 bell peppers, cubed
4 dried red chilies
3 cloves garlic, minced
2 tbsp soy sauce
1 tbsp rice vinegar
1 tbsp sugar
2 tsp cornstarch
2 tbsp vegetable oil
Green onions for garnish''',
                'instructions': '''1. Mix soy sauce, vinegar, sugar, and cornstarch in a bowl.
2. Heat oil in a wok over high heat.
3. Stir-fry chicken until cooked through, set aside.
4. Add chilies and garlic, stir-fry for 30 seconds.
5. Add bell peppers and cook for 2 minutes.
6. Return chicken to wok with sauce mixture.
7. Stir until sauce thickens.
8. Add peanuts and toss to combine.
9. Garnish with green onions and serve with rice.''',
                'prep_time': 15,
                'cook_time': 15,
                'servings': 4,
                'difficulty': 'medium',
                'status': 'published'
            },
            {
                'title': 'Fluffy Buttermilk Pancakes',
                'category': 'Breakfast',
                'country': 'Italian',
                'description': 'Fluffy, golden pancakes perfect for a weekend breakfast.',
                'ingredients': '''200g all-purpose flour
2 tbsp sugar
2 tsp baking powder
1/2 tsp salt
1 egg
300ml buttermilk
2 tbsp melted butter
Butter for cooking
Maple syrup for serving
Fresh berries (optional)''',
                'instructions': '''1. Whisk together flour, sugar, baking powder, and salt.
2. In another bowl, beat egg with buttermilk and melted butter.
3. Pour wet ingredients into dry and mix until just combined (lumps are okay).
4. Heat a non-stick pan over medium heat and add butter.
5. Pour 1/4 cup batter for each pancake.
6. Cook until bubbles form on surface, then flip.
7. Cook until golden brown on both sides.
8. Serve warm with maple syrup and fresh berries.''',
                'prep_time': 10,
                'cook_time': 20,
                'servings': 4,
                'difficulty': 'easy',
                'status': 'published'
            },
            {
                'title': 'Chicken Caesar Salad',
                'category': 'Lunch',
                'country': 'Italian',
                'description': 'Crisp romaine lettuce with grilled chicken, parmesan, and Caesar dressing.',
                'ingredients': '''2 chicken breasts
1 large head romaine lettuce
100g parmesan cheese, shaved
1 cup croutons
For dressing:
3 cloves garlic
2 anchovy fillets
1 egg yolk
2 tbsp lemon juice
1 tsp Dijon mustard
150ml olive oil
Salt and pepper''',
                'instructions': '''1. Season and grill chicken breasts until cooked through. Slice.
2. For dressing: blend garlic, anchovies, egg yolk, lemon juice, and mustard.
3. Slowly drizzle in olive oil while blending until thick.
4. Season with salt and pepper.
5. Chop romaine lettuce and place in a large bowl.
6. Add sliced chicken, croutons, and parmesan.
7. Toss with dressing and serve immediately.''',
                'prep_time': 15,
                'cook_time': 15,
                'servings': 2,
                'difficulty': 'easy',
                'status': 'published'
            },
            {
                'title': 'Chocolate Chip Cookies',
                'category': 'Dessert',
                'country': 'Italian',
                'description': 'Classic chewy chocolate chip cookies with crispy edges.',
                'ingredients': '''225g butter, softened
200g brown sugar
100g granulated sugar
2 eggs
2 tsp vanilla extract
280g all-purpose flour
1 tsp baking soda
1 tsp salt
300g chocolate chips''',
                'instructions': '''1. Preheat oven to 180°C (350°F).
2. Cream together butter and sugars until fluffy.
3. Beat in eggs and vanilla.
4. In separate bowl, whisk flour, baking soda, and salt.
5. Gradually mix dry ingredients into wet mixture.
6. Fold in chocolate chips.
7. Drop rounded tablespoons of dough onto baking sheets.
8. Bake for 10-12 minutes until edges are golden.
9. Cool on baking sheet for 5 minutes before transferring to wire rack.''',
                'prep_time': 15,
                'cook_time': 12,
                'servings': 24,
                'difficulty': 'easy',
                'status': 'published'
            },
            {
                'title': 'Tiramisu',
                'category': 'Dessert',
                'country': 'Italian',
                'description': 'Classic Italian dessert with coffee-soaked ladyfingers and mascarpone cream.',
                'ingredients': '''6 egg yolks
150g sugar
500g mascarpone cheese
300ml strong espresso, cooled
3 tbsp coffee liqueur (optional)
300g ladyfinger biscuits
Cocoa powder for dusting
Dark chocolate shavings (optional)''',
                'instructions': '''1. Whisk egg yolks and sugar until thick and pale.
2. Add mascarpone and beat until smooth.
3. Mix espresso with coffee liqueur in a shallow dish.
4. Quickly dip ladyfingers in coffee mixture (don't soak).
5. Arrange layer of dipped ladyfingers in a dish.
6. Spread half the mascarpone mixture over biscuits.
7. Repeat with another layer of dipped ladyfingers and cream.
8. Refrigerate for at least 4 hours or overnight.
9. Dust with cocoa powder before serving.''',
                'prep_time': 30,
                'cook_time': 0,
                'servings': 8,
                'difficulty': 'medium',
                'status': 'published'
            },
        ]

        # Create recipes
        for recipe_data in recipes_data:
            category, _ = Category.objects.get_or_create(
                name=recipe_data['category'],
                defaults={'slug': slugify(recipe_data['category'])}
            )
            
            country, _ = Country.objects.get_or_create(
                name=recipe_data['country'],
                defaults={'slug': slugify(recipe_data['country'])}
            )
            
            recipe, created = Recipe.objects.get_or_create(
                title=recipe_data['title'],
                defaults={
                    'slug': slugify(recipe_data['title']),
                    'author': admin_user,
                    'category': category,
                    'country': country,
                    'description': recipe_data['description'],
                    'ingredients': recipe_data['ingredients'],
                    'instructions': recipe_data['instructions'],
                    'prep_time': recipe_data['prep_time'],
                    'cook_time': recipe_data['cook_time'],
                    'servings': recipe_data['servings'],
                    'difficulty': recipe_data['difficulty'],
                    'status': recipe_data['status']
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created recipe: {recipe.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Recipe already exists: {recipe.title}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated recipes!'))
