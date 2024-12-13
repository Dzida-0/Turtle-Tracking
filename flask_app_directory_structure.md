# Improved Flask Application Directory Structure

```
flask_app/
├── app/
│   ├── __init__.py             # Initialize Flask app, register blueprints, config, and extensions
│   ├── forms.py                # All Flask-WTF forms
│   ├── models.py               # All SQLAlchemy models (Users, Turtles, TurtlesMoves, UsersLikeTurtles)
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
│   │   ├── turtles.html        # List of turtles and user likes
│   │   ├── turtle.html         # Detailed view of a single turtle with map
│   │   ├── error/              # Error templates folder
│   │   │   ├── error_404.html  # 404 error page
│   │   │   ├── error_500.html  # 500 error page
│   ├── static/
│       ├── css/
│       │   ├── style.css       # Main CSS styles
│       ├── images/             # Any images or icons
│       ├── maps/               # GeoJSON or map data (generated dynamically if needed)
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
│   ├── test_turtles.py         # Test for turtles functionality
├── config.py                   # Configuration settings (e.g., dev, prod)
├── run.py                      # Main entry point to run the application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
```

---

## **Database Tables**

### 1. `Users`
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password`: Hashed password

### 2. `Turtles`
- `id`: Primary key
- `name`: Turtle name
- `species`: Turtle species
- `status`: Conservation status (e.g., Endangered)

### 3. `TurtlesMoves`
- `id`: Primary key
- `turtle_id`: Foreign key to `Turtles`
- `timestamp`: Timestamp of the recorded move
- `latitude`: Latitude position
- `longitude`: Longitude position

### 4. `UsersLikeTurtles`
- `id`: Primary key
- `user_id`: Foreign key to `Users`
- `turtle_id`: Foreign key to `Turtles`

---

## **Page Details**

### 1. **`/turtles` Page**
- Displays a table with all turtles and their attributes.
- Includes a custom checkbox for users to indicate if they like a specific turtle.
- Data is dynamically fetched from the `Turtles` and `UsersLikeTurtles` tables.

### 2. **`/turtle/<id>` Page**
- Displays detailed information about a single turtle using data from the `Turtles` table.
- Includes a movable map (using GeoPandas) showing the turtle's movements.
  - Data is fetched from the `TurtlesMoves` table and plotted dynamically.
- Provides additional insights like most frequently visited areas or distance traveled.

---

## **Key Features of Structure**

1. **GeoPandas Integration**
   - Data for turtle movements is stored in the `TurtlesMoves` table.
   - Maps are dynamically generated and rendered as images or interactive components.

2. **Temporary JSON Handling**
   - `data_download.py` fetches turtle data and creates a temporary JSON file.
   - `data_parse.py` reads and processes the JSON to update the database or generate reports.

3. **Error Handling**
   - Dedicated error templates (`error_404.html`, `error_500.html`) are used for user-friendly error messages.

4. **Modular Code Organization**
   - Blueprints in the `routes/` folder separate functionality by domain.
   - Database models and forms are organized in `models.py` and `forms.py` respectively.

5. **Testing Framework**
   - Unit and integration tests in the `tests/` folder ensure functionality for routes, authentication, and database operations.

---

Would you like to see example implementations for any of the above components?
