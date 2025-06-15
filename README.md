DevFlow Manager — Software Engineering Assignment (DataX.ai)
A full-stack Django application with:
- Project & Task Management API
- User Action Logging
- CLI Image Processing Tool

Built to demonstrate proficiency in backend development, RESTful APIs, middleware, and Python scripting.
Tech Stack
- Backend: Django 5.x, Django REST Framework
- Database: SQLite3
- Image Processing: Python (Pillow, Requests)
- Authentication: Token Auth (DRF)
- Logging: Custom Middleware
Features
Task 1: Project Management System (Django + DRF)
- CRUD for Projects and nested Tasks
- Pagination + filtering (name, start_date, end_date)
- CSV download of project data
- Soft delete projects (preserved in DB)
- Image upload for projects
- Authenticated API access
Task 2: User Action Logging
- Middleware logs POST, PUT, and DELETE operations
- Captures user, action (method + path), timestamp, IP address
- View logs via Django Admin
Task 3: CLI Image Processor
- Input: Single image URL or CSV of URLs
- Output: JSON file with base64 original + resized image (320x568), image size and resolution
- Error-handling with per-image status reporting
Getting Started
Backend Setup:
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
Auth:
POST /api/token-auth/ — Use Authorization: Token <your_token>
CLI Tool Usage (image_processor.py)
Run for single image:
python image_processor.py --url https://upload.wikimedia.org/wikipedia/commons/9/99/Sample_User_Icon.png
Run for CSV of image URLs:
python image_processor.py --csv images.csv
Sample Output (image_output.json)
[
  {
    "image_url": "...",
    "status": "success",
    "resolution": "1024x768",
    "size": 18345,
    "original_image64": "....",
    "resized_image64": "...."
  }
]
Sample CSV (images.csv)
https://upload.wikimedia.org/wikipedia/commons/9/99/Sample_User_Icon.png
https://www.w3schools.com/w3images/fjords.jpg
https://www.w3schools.com/w3images/lights.jpg
Project Structure
image_processor.py         # CLI image tool
images.csv                 # Sample input
image_output.json          # Output of CLI
projects/                  # Django app
project_management/        # Django settings/urls
manage.py
db.sqlite3
requirements.txt
README.md
Requirements
pip install -r requirements.txt
Key libraries: Django, djangorestframework, pillow, requests
Author
Divyodai Singh — Computer Science Engineer | Backend & AI | VIT Graduate
License
This project is for educational and evaluation purposes only.
