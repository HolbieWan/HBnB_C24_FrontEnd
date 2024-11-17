![alt text](<images/Capture d’écran 2024-11-17 à 21.38.05.png>)

# **HBnB_App**

HBnB is a web-based application that allows users to explore places, add reviews, and manage amenities, places, and users. The app includes both a front-end interface and a RESTful API for backend operations.

---

## **Features**

### Frontend
- **Homepage (`/HBnB`)**: Displays a list of available places with their details.
- **Place Details (`/HBnB/place`)**: Displays specific place details, allows users to add reviews, and view reviews left by others.
- **Login (`/HBnB/login`)**: Users can log in to access protected features.
- **Add Review (`/HBnB/add_review`)**: Authenticated users can add reviews to places.

### Backend
- **User Management**: Create, read, update, and delete user accounts.
- **Place Management**: Add and manage places, including details like price and location.
- **Review Management**: Users can post reviews and ratings for places.
- **Amenity Management**: Manage amenities associated with places.
- **Authentication**: User login and logout functionality with JWT-based authentication.
- **Blueprints and RESTful API**: Structured backend with modular routes for frontend and API namespaces.

---

## **Setup Instructions**

### Prerequisites
- Python 3.10+
- Flask
- Node.js (for managing static files, if necessary)
- A compatible database (e.g., SQLite or PostgreSQL)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/HBnB.git
   cd HBnB
   ```
2.	**Create a Virtual Environment**
    ```bash
    python3 -m venv HBnBenv
    source HBnBenv/bin/activate
    ```
3.	**Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ````
4. **Configure Environment Variables**
    ```bash
    export FLASK_ENV=development
    export DATABASE_URL="sqlite:///development.db"
    ```

5.	**Set Up the Database**
+ Create and configure the database:

    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ````
6. **Create a Superuser**
    ```bash
    python3 utils/manage.py create_superuser
    ```
7.	**Start the Development Server**

    ```bash
    python3 run.py
    ```
8.	**Navigate to the App**
+ Open your browser and visit:
+ Frontend: http://127.0.0.1:5000/HBnB
+ API Docs: http://127.0.0.1:5000

9. **Testing**

+ Run the tests:

    ```bash
    python3 run_coverage.py
    ```

## **Folder Structure**

```bash
HBnB_C24_FRONTEND/
│
├── app/
│   ├── api/               # API routes for the application
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── routes_users.py
│   │   │   ├── routes_places.py
│   │   │   ├── routes_amenities.py
│   │   │   ├── routes_reviews.py
│   │   │   ├── routes_login.py
│   │   │   ├── routes_FrontEnd.py
│   │   ├── __init__.py
│   │
│   ├── models/            # Models for database entities
│   │   ├── __init__.py
│   │   ├── base_model.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   │
│   ├── persistence/       # Persistence logic for repositories
│   │   ├── __init__.py
│   │   ├── repository.py
│   │
│   ├── services/          # Application service logic
│   │   ├── __init__.py
│   │   ├── facade.py
│   │
│   ├── static/            # Static files (CSS, JS, images)
│   │   ├── styles.css
│   │   ├── auth_links.js
│   │   ├── add_review.js
│   │   ├── fetch_place_details.js
│   │   ├── get_all_places.js
│   │   ├── images/
│   │       ├── logo.png
│   │       ├── icon.png
│   │
│   ├── templates/         # HTML templates
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── place.html
│   │   ├── add_review.html
│   │
│   ├── tests/             # Unit tests for the app
│   │   ├── __init__.py
│   │   ├── test_users.py
│   │   ├── test_places.py
│   │
│   ├── __init__.py        # App initialization
│   ├── extensions.py      # Flask extensions
│
├── coverage/              # Test coverage reports
│
├── HBnBenv/               # Virtual environment directory
│
├── images/                # Additional documentation images
│
├── instance/              # Instance-specific configuration
│
├── mermaid/               # Diagrams for the project
│
├── migrations/            # Flask-Migrate database migrations
│
├── SQL_DB_Setup/          # SQL database setup scripts
│
├── utils/                 # Utility scripts for the app
│   ├── manage.py          # CLI management commands
│   ├── create_super_user.py
│
├── .coverage              # Test coverage file
├── .coveragerc            # Coverage configuration file
├── .gitignore             # Git ignore rules
├── config.py              # App configuration
├── README.md              # Project documentation
├── requirements.txt       # Project dependencies
├── run.py                 # Start the Flask application
├── run_coverage.py        # Run coverage tests
```

## **Mermaid Database Schema**

![Capture d’écran 2024-11-11 à 22.21.04.png](<images/Capture d’écran 2024-11-11 à 22.21.04.png>)

## **Frontend Functionality**

**Authentication**

+ Users can log in with their email and password.
+ JWT tokens are stored as secure cookies for making authenticated API requests.

**Adding Reviews**

+ Authenticated users can add reviews to places
+ with a rating between 1 and 5.
+ Example data sent via POST:


    ```bash
    {
    "user_id": "12345",
    "place_id": "67890",
    "text": "Great place to stay!",
    "rating": 5
    }
    ```
**Fetching Reviews**

+ Reviews for a specific place are dynamically fetched and displayed using JavaScript.

## **Backend Implementation**

**Modular Design**

+ Blueprints: The frontend and API routes are organized using Flask Blueprints for modularity.

+ Service Layer: The facade.py file implements the core logic for interacting with models and performing operations.

+ RESTful API: Flask-RESTx is used for clean and structured API routes, complete with Swagger documentation.

**Database Models**

+ User Model: Stores user information such as name, email, and hashed passwords.
+ Place Model: Contains details about a place (e.g., title, price, and amenities).
+ Review Model: Stores user reviews with a rating for a specific place.
+ Amenity Model: Manages amenities associated with places.

## **Contributing**

	1.	Fork the repository.
	2.	Create a new branch (git checkout -b feature-branch).
	3.	Commit changes (git commit -m "Add feature").
	4.	Push to the branch (git push origin feature-branch).
	5.	Open a pull request.

**Authentication**

+ Login: Users authenticate via /api/v1/login/ and receive a JWT token.

+ Logout: The token is invalidated by clearing cookies via /api/v1/auth/logout.

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.