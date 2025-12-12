# Database Schema - Entity Relationship Diagram

```mermaid
erDiagram
    User ||--o{ Recipe : "creates"
    User ||--o{ Comment : "writes"
    User ||--o{ Like : "favorites"
    
    Recipe ||--o{ Comment : "has"
    Recipe ||--o{ Like : "has"
    Recipe }o--|| Category : "belongs to"
    Recipe }o--|| Country : "from"
    
    User {
        int id PK
        string username UK
        string email UK
        string password
        datetime date_joined
    }
    
    Recipe {
        int id PK
        string title
        string slug UK
        text description
        text ingredients
        text instructions
        int prep_time
        int cook_time
        int servings
        string difficulty
        string status
        image image
        int author_id FK
        int category_id FK
        int country_id FK
        datetime created_at
        datetime updated_at
    }
    
    Category {
        int id PK
        string name UK
        string slug UK
        text description
    }
    
    Country {
        int id PK
        string name UK
        string slug UK
    }
    
    Comment {
        int id PK
        text content
        int recipe_id FK
        int user_id FK
        datetime created_at
        datetime updated_at
    }
    
    Like {
        int id PK
        int recipe_id FK
        int user_id FK
        datetime created_at
    }
```

## Model Relationships

### **User Model** (Django built-in)
- **One-to-Many** with Recipe (one user creates many recipes)
- **One-to-Many** with Comment (one user writes many comments)
- **One-to-Many** with Like (one user likes many recipes)

### **Recipe Model**
- **Many-to-One** with User (many recipes belong to one author)
- **Many-to-One** with Category (many recipes in one category)
- **Many-to-One** with Country (many recipes from one country)
- **One-to-Many** with Comment (one recipe has many comments)
- **One-to-Many** with Like (one recipe has many likes)

### **Category Model**
- **One-to-Many** with Recipe (one category has many recipes)

### **Country Model**
- **One-to-Many** with Recipe (one country has many recipes)

### **Comment Model**
- **Many-to-One** with Recipe (many comments on one recipe)
- **Many-to-One** with User (many comments by one user)

### **Like Model**
- **Many-to-One** with Recipe (many likes on one recipe)
- **Many-to-One** with User (many likes by one user)
- **Unique Constraint**: One user can only like a recipe once

## Key Features
- **Cascading Deletes**: When a recipe is deleted, all associated comments and likes are deleted
- **Unique Constraints**: Usernames, emails, slugs are unique
- **Status Field**: Recipes can be 'draft' or 'published'
- **Timestamps**: All models track creation and update times
