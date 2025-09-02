Healthcare Platform

A web-based healthcare platform built with Flask, SQLite, and modern front-end technologies. The platform allows users to track their health, book appointments, view health-related articles, watch wellness videos, and maintain personal profiles and mood entries.

Features

User Profile: Users can create and update personal health profiles including age, gender, sleep hours, activity levels, and notes.

Appointments: Users can book, view, and manage doctor appointments.

Mood Tracker: Track daily moods with scores and optional notes.

Health Articles: Access curated health and wellness articles.

Health Videos: Watch wellness and fitness videos embedded from YouTube.

Recipes: Discover healthy recipes with step-by-step instructions.

Dashboard: Overview of health data, mood entries, and suggestions for well-being.

API Support: REST API endpoint for fetching mood entries in JSON format and others

Technologies Used

Backend: Python, Flask

Database: SQLite (via SQLAlchemy ORM)

Frontend: HTML, CSS, JavaScript

Templating: Jinja2 (Flask templates)

Installation

Clone the repository

git clone https://github.com/yourusername/healthcare-platform.git
cd healthcare-platform


Create a virtual environment

python -m venv venv


Activate the virtual environment

On Windows:

venv\Scripts\activate


On Mac/Linux:

source venv/bin/activate


Install dependencies

pip install -r requirements.txt


Run the application

python app.py


Open a browser and visit http://127.0.0.1:5000/

Project Structure
healthcare-platform/
│
├─ app.py                 # Main Flask application
├─ health_platform.db     # SQLite database file (auto-created)
├─ templates/             # HTML templates
│   ├─ base.html
│   ├─ index.html
│   ├─ about.html
│   ├─ videos.html
│   ├─ articles.html
│   ├─ recipes.html
│   ├─ appointments.html
│   ├─ book_appointment.html
│   └─ ...
├─ static/                # Static files (CSS, JS, images)
│   └─ style.css
├─ requirements.txt       # Python dependencies
└─ README.md

API Endpoints

GET /api/mood_entries
Returns a JSON list of all mood entries:

[
  {"date": "2025-09-01", "score": 7},
  {"date": "2025-09-02", "score": 6}
]

Usage

Navigate through the horizontal navigation bar to access Home, Videos, Articles, Recipes, Appointments, and Profile.

Book doctor appointments and track upcoming or past appointments.

Record daily mood entries for self-assessment.

View wellness articles and videos for health guidance.
