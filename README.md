# GPO Document Gateway

A REST API for managing federal government documents through their full publication lifecycle. Built with Django and Django REST Framework.

## Tech Stack

- Python 3.13 / Django 6.0 / Django REST Framework 3.17
- SQLite (dev) — PostgreSQL-ready via `DATABASE_URL`
- django-filter, django-cors-headers, python-dotenv

## Getting Started

```powershell
# From legacy-api/
.venv\Scripts\activate

python manage.py migrate
python manage.py seed_data   # optional: loads sample documents
python manage.py runserver
```

The API is available at `http://localhost:8000/api/`.

## Environment Variables

Copy `.env` and adjust as needed. The app reads these from `legacy-api/.env`:

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | insecure dev key | Django secret key |
| `DEBUG` | `True` | Debug mode |
| `DATABASE_URL` | `sqlite:///db.sqlite3` | Database connection string |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated allowed hosts |

## API Endpoints

Base path: `/api/`

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

### Status Transition

```http
POST /api/documents/{id}/transition/
Content-Type: application/json

{
  "status": "review",
  "changed_by": "editor@gpo.gov",
  "notes": "Ready for editorial review"
}
```

Valid statuses: `draft` → `review` → `approved` → `published` → `archived`

Every transition is recorded in `StatusHistory` for a full audit trail.

### Filtering & Search

Documents support filtering (`?status=draft&category=1`), full-text search (`?search=federal+register`), and ordering (`?ordering=-submitted_date`). Authors can be filtered by `?agency=`.

### Pagination

All list endpoints return paginated results (20 per page). Use `?page=2` to navigate.

## Django Admin

Available at `/admin/`. Create a superuser first:

```powershell
python manage.py createsuperuser
```
