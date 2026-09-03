# Smart_season

SmartSeason Field Monitoring System

## Quickstart (development)

1. Clone the repository

```bash
git clone https://github.com/georgebrian7/Smart_season.git
cd Smart_season
```

2. Create and activate a Python virtual environment

```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. (Optional) Create a .env file at the project root to override defaults. See `.env.example` for suggested variables.

5. Apply migrations and run the development server

```bash
python manage.py migrate
python manage.py createsuperuser   # optional
python manage.py runserver
```

6. Open http://127.0.0.1:8000/ in your browser.

Notes
- This is a Django project. The README previously referenced `python app.py` which is not applicable — use `manage.py` as shown above.
- The project ships a local sqlite database (`db.sqlite3`) for convenience in development. For production, set `DATABASE_URL` to a Postgres (or other) database in your environment.

