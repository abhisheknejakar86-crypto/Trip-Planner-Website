# TripPlannerWebsite

A Django MVT project for planning holidays, booking hotels, choosing travel options, and requesting trip packages. It uses SQLite by default, so it is easy to run in a local environment.

## Features

- Destination, hotel, transport, package, and booking models
- Responsive pages using Django templates
- Professional service search for flights, hotels, trains, buses, cabs, and packages
- Search results page with left-side filters
- Domestic and international demo inventory
- Custom TravelMate logo
- Mobile navigation with JavaScript
- Live card search and sorting
- Transport table filtering
- Trip checklist progress bar
- Booking form helper summary
- Local saved trips using browser storage
- Signup, login, logout, and remember-me option
- Private user booking history and explored-plan history
- Demo data command for quick setup

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in the browser.

## Admin Login

Create an admin user with:

```powershell
python manage.py createsuperuser
```

Then visit `http://127.0.0.1:8000/admin/`.
