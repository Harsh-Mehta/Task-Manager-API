# Task-Manager-API

## Introduction
This is a simple Task Manager API built for effectively managing the task and keeping a track of them.

## Features
- Create tasks
- Retrieve a list of all tasks with filtering option on completion status
- Retrieve details of a specific task
- Modify tasks
- Delete tasks

## Technology
- FastAPI
- SQLite
- SQLAlchemy
- Alembic
- Pytest

## File Structure
```
.
├── alembic/                   # Alembic migration directory
├── alembic.ini                # Alembic configuration file
├── db                         # SQLite databases
├── poetry.lock                # Poetry lock file
├── pyproject.toml             # Poetry configuration file
├── README.md                  # Project README file
├── src/
│   ├── config.py              # Global configuration file
│   ├── database.py            # Database connection setup
│   ├── __init__.py            # Package initialization
│   ├── main.py                # Application entry point
│   ├── models.py              # Global database models
│   └── tasks/                 # Task-related modules
│       ├── crud.py            # CRUD operations
│       ├── models.py          # Task models
│       ├── router.py          # Task API routes
│       ├── schemas.py         # Task schemas
│       └── utils.py           # Utility functions
└── tests/
    ├── conftest.py            # Test configuration
    ├── __init__.py            # Test package initialization
    └── test_tasks.py          # Task tests
```

## Usage

### Pre-requisites
- Ensure the Python (>=3.12) and Poetry are installed 

### Running the application
1. Clone the repository:  
```git clone <respository-url>```

2. Navigate to the project root directory:  
```cd Task-Manager-API```

3. (Optional) Create a virtual environment:  
```poetry shell```

4. Install the project dependencies:  
```poetry install```

5. Run the migrations to create the database and the tables:  
```peotry run alembic upgrade head```

6. Run the application:  
```poetry run uvicorn src.main:app```

7. Run the tests:  
```poetry run pytest```

The application will be running on ```http://localhost:8000```

### Creating a new migration
1. Create a new migration:  
```poetry run alembic revision --autogenerate -m "description"```

2. Run the migration:  
```peotry run alembic upgrade head```