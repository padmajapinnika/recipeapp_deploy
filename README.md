# 🥘 Recipe App

## Overview

The Recipe App is a fully functional web application designed to allow users to create, read, and view recipes, as well as search for recipes based on ingredients. Built with Python and Django, this app demonstrates the capabilities of modern web development, including dynamic content rendering, database integration, and static/media file handling. It is deployed on Heroku and showcases the developer's understanding of the Django web framework.

> **Note:** Images may not display correctly in the deployed version due to Heroku's free-tier limitations on dynamic media storage.

---

## 🔧 Technical Requirements

- Python 3.6+ and Django 4.2 compatibility
- PostgreSQL for production (Heroku) and SQLite for local development
- Exception handling with user-friendly error messages
- Static and media file management via `STATICFILES_DIRS` and `MEDIA_ROOT`
- Well-structured codebase with modular apps
- Includes `requirements.txt` for easy setup

---

## ✨ Key Features

- 📋 Display list of recipes with names, ingredients, and preparation steps
- 🔍 Recipe search by ingredient (partial match supported)
- 🖼 Recipe image upload and display (served from `/media/`)
- 👤 Django Admin dashboard for managing recipe entries
- ⚠️ Error handling for missing data and invalid input
- 📊 Scalable structure for future enhancements (e.g., difficulty ratings, stats)

---

## 🎯 User Goals

- View and search for recipes by ingredients
- Explore recipe details including images, steps, and ingredients
- Admin users can add, update, and delete recipes through the admin interface
- Eventually, support for user submissions and interaction (in future)

## 🚀 Setup and Installation

### 1. Clone the Repository

git clone https://github.com/your-username/recipeapp.git
cd recipeapp_deploy

### 2. Install Dependencies

pip install -r requirements.txt

### 3. Set Up the Database

Adjust the DATABASES configuration in settings.py:

Use SQLite for development (default)

Use PostgreSQL on Heroku (automatically configured with dj_database_url)

### 4. Apply Migrations

python manage.py migrate

### 5. Create Superuser

python manage.py createsuperuser

### 6. Run the Development Server

python manage.py runserver
Visit http://127.0.0.1:8000 in your browser to view the app.

☁️ Heroku Deployment Notes
Add Heroku PostgreSQL:

heroku addons:create heroku-postgresql --app your-app-name
Push code and migrate database:

git push heroku main
heroku run python manage.py migrate
Create a superuser:

heroku run python manage.py createsuperuser
Media files are not stored persistently on Heroku free tier. In the future, consider integrating AWS S3 or Cloudinary for media storage.

## 📌 Future Enhancements

Integrate AWS S3 for persistent image storage

Add user authentication and public recipe submission

Implement recipe difficulty rating and tags

Add filtering/sorting by cooking time, type, etc.

Add unit tests

👩‍💻 Author
Padmaja
