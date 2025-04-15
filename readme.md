# Library Management System

This project contains three microservices built with Flask for managing a library system. The services include:

- **Authentication Service** (`auth_service.py`)
- **Book Management Service** (`book_service.py`)
- **Rental Service** (`rental_service.py`)

## Setup Instructions

### Create the Virtual Environment

### Split the terminal

```bash
python Database/int_db.py
python auth_service.py
python book_service.py
python rental_service.py
```

Open your web browser and navigate to the authentication service (e.g., http://localhost:5505) to start the registration and login process. After logging in, follow the dashboard links to access book management and rental services.

## Note

Session management is not properly done
