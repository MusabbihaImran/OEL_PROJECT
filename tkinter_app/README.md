# Hotel Booking and Room Management System

A complete, fully functional Hotel Booking and Room Management System built with Python 3, Tkinter, and SQLite.

## Prerequisites
- Python 3.10+
- SQLite is built into Python, no external database server is required.

## Setup Steps
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `python -m app.main`
   - *Note: On the first run, the SQLite database (`hotel.db`) will be created automatically and populated with seed data.*

## Folder Structure
- `app/`: Contains the main application logic
  - `views/`: Tkinter GUI screens
  - `models/`: Database interaction layer
  - `services/`: Business logic layer
  - `utils/`: Reusable constants, styling, and validation
  - `init_db.py`: Automated database initialization
- `tests/`: Unit tests for services and views
- `schema.sql`: Database table definitions and seed data
- `hotel.db`: SQLite database file (created automatically on first run)

## Testing
Run tests using:
```bash
python -m unittest discover tests
```

## Authors
SEC6402_SCD, OEL submission
