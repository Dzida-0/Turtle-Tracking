
# Flask Application Directory Structure

```
flask_app/
├── app/
│   ├── __init__.py             # Initialize Flask app, register blueprints, config, and extensions
│   ├── forms.py                # All Flask-WTF forms
│   ├── models.py               # All SQLAlchemy models
│   ├── routes/
│   │   ├── __init__.py         # Blueprint registration
│   │   ├── main.py             # Main routes for the app
│   │   ├── turtles.py          # Routes specific to turtles
│   │   ├── auth.py             # Authentication-related routes
│   ├── templates/
│   │   ├── base.html           # Main base template
│   │   ├── index.html          # Homepage
│   │   ├── login.html          # Login page
│   │   ├── register.html       # Registration page
│   │   ├── turtles.html        # List of turtles
│   │   ├── turtle.html         # Details of a single turtle
│   │   ├── error/              # Error templates folder
│   │   │   ├── error_404.html  # 404 error page
│   │   │   ├── error_500.html  # 500 error page
│   ├── static/
│       ├── css/
│       │   ├── style.css       # Main CSS styles
│       ├── images/             # Any images or icons
├── data/
│   ├── data_download.py        # Script to download data and create a temporary JSON file
│   ├── data_parse.py           # Script to parse and process the downloaded JSON file
│   ├── temp/                   # Temporary storage for JSON files
│       ├── temp_data.json      # Temporary JSON file created by data_download.py
├── instance/
│   ├── database.db             # SQLite database (can also use MySQL/PostgreSQL if needed)
├── migrations/                 # Database migrations (created with Flask-Migrate)
├── tests/                      # Unit and integration tests
│   ├── test_main.py            # Test for main routes
│   ├── test_auth.py            # Test for authentication
├── config.py                   # Configuration settings (e.g., dev, prod)
├── run.py                      # Main entry point to run the application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
```
