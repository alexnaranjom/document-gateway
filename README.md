# GPO Document Gateway

A system for managing federal government documents through their full publication lifecycle. Composed of two services:

- **`legacy-api/`** — Django REST API; the authoritative data store and lifecycle engine
- **`middleware/`** — FastAPI async proxy that sits in front of the Django API, adding authentication and a clean async interface

## Tech Stack

**legacy-api**
- Python 3.13 / Django 6.0 / Django REST Framework 3.17
- SQLite (dev) — PostgreSQL-ready via `DATABASE_URL`
- django-filter, django-cors-headers, python-dotenv

**middleware**
- Python 3.13 / FastAPI / Uvicorn
- httpx (async HTTP client), Pydantic, python-dotenv

## Getting Started

### legacy-api (Django)

```powershell
# From legacy-api/
.venv\Scripts\activate
python manage.py migrate
python manage.py seed_data   # optional: loads sample documents
python manage.py runserver   # http://localhost:8000
```

### middleware (FastAPI)

```powershell
# From middleware/
.venv\Scripts\activate
uvicorn main:app --reload    # http://localhost:8001
```

## Environment Variables

**`legacy-api/.env`**

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | `django-insecure-local-dev-key` | Django secret key |
| `DEBUG` | `True` | Debug mode |
| `DATABASE_URL` | `sqlite:///db.sqlite3` | Database connection string |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated allowed hosts |

**`middleware/.env`**

| Variable | Default | Description |
|---|---|---|
| `LEGACY_API_URL` | `http://127.0.0.1:8000/api` | Django API base URL |
| `API_KEY` | `dev-api-key-change-in-production` | Middleware auth key |

## API Endpoints

Base path: `/api/` (legacy-api, port 8000)

| Method | Endpoint | Description |
|---|---|---|
| GET/POST | `/api/categories/` | List or create document categories |
| GET/PUT/DELETE | `/api/categories/{id}/` | Retrieve, update, or delete a category |
| GET/POST | `/api/authors/` | List or create authors |
| GET/PUT/DELETE | `/api/authors/{id}/` | Retrieve, update, or delete an author |
| GET/POST | `/api/documents/` | List or create documents |
| GET/PUT/DELETE | `/api/documents/{id}/` | Retrieve, update, or delete a document |
| POST | `/api/documents/{id}/transition/` | Transition document status |
| GET | `/api/documents/stats/` | Aggregate counts by status |

### Status Lifecycle

```
draft → review → approved → published → archived
```

```http
POST /api/documents/{id}/transition/
Content-Type: application/json

{
  "status": "review",
  "changed_by": "editor@gpo.gov",
  "notes": "Ready for editorial review"
}
```

Every transition is recorded in `StatusHistory` for a full audit trail.

### Filtering & Search

Documents support filtering (`?status=draft&category=1`), full-text search (`?search=federal+register`), and ordering (`?ordering=-submitted_date`). Authors can be filtered by `?agency=`. All list endpoints are paginated (20 per page).

## Django Admin

Available at `/admin/` (legacy-api). Create a superuser first:

```powershell
python manage.py createsuperuser
```
