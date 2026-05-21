# Handover Document — Devangwa Coaching Application

## Overview

Devangwa is a monorepo with:

- **Backend:** Django 4.2 + Django REST Framework (`devangwabackend/`)
- **Frontend:** Vue 3 + Vite (`devangwacoaching/`)
- **Deployment:** Single Docker image (Nginx + Gunicorn + built SPA)

## Documentation index

| File | Audience |
|------|----------|
| [../README.md](../README.md) | Monorepo quick start |
| [README.md](README.md) | Platform overview |
| [BACKEND_README.md](BACKEND_README.md) | Backend developers |
| [FRONTEND_README.md](FRONTEND_README.md) | Frontend developers |
| [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) | API consumers |
| [../devangwacoaching/README.md](../devangwacoaching/README.md) | Frontend dev setup |

## Build and run (Docker)

### Prerequisites

- Docker
- Monorepo cloned with both `devangwabackend/` and `devangwacoaching/`

### Build

Run from the **repository root** (parent of both apps):

```bash
docker build -f devangwabackend/Dockerfile -t devangwa-app .
```

The Dockerfile:

1. Builds the Vue app (`npm run build`)
2. Copies `dist/` into Django `static/` and `templates/`
3. Installs Python dependencies
4. Configures Nginx to serve static/media and proxy `/api/` to Gunicorn

Migrations and `collectstatic` run on container start via `docker-entrypoint.sh`.

### Run

```bash
docker run -p 80:80 \
  -e DEBUG=False \
  -e SECRET_KEY=your-secure-secret-key \
  -e ALLOWED_HOSTS=yourdomain.com,localhost \
  -e DATABASE_ENGINE=django.db.backends.postgresql \
  -e DATABASE_NAME=devangwa \
  -e DATABASE_USER=devangwa \
  -e DATABASE_PASSWORD=change-me \
  -e DATABASE_HOST=db-host \
  -e DATABASE_PORT=5432 \
  -e CORS_ALLOWED_ORIGINS=https://yourdomain.com \
  -e CSRF_TRUSTED_ORIGINS=https://yourdomain.com \
  -e PAYMENTS_API_BASE_URL=https://yourdomain.com/api/v1/payments \
  -e EMAIL_HOST=smtp.gmail.com \
  -e EMAIL_PORT=587 \
  -e EMAIL_USE_TLS=True \
  -e EMAIL_HOST_USER=your-email@gmail.com \
  -e EMAIL_HOST_PASSWORD=your-app-password \
  -e SENTRY_DSN=your-sentry-dsn \
  devangwa-app
```

### URLs

| URL | Purpose |
|-----|---------|
| `/` | Vue SPA |
| `/api/v1/` | REST API |
| `/health/` | Load balancer health check |
| `/api/v1/admin/` | Django admin |

## Environment variables

Use `devangwabackend/.env.example` as the template. Critical variables:

| Variable | Notes |
|----------|--------|
| `SECRET_KEY` | Required in production; app refuses default when `DEBUG=False` |
| `DEBUG` | `False` in production |
| `ALLOWED_HOSTS` | Comma-separated |
| `PAYMENTS_API_BASE_URL` | Must include `/api/v1/payments` path |
| `CORS_ALLOWED_ORIGINS` / `CSRF_TRUSTED_ORIGINS` | Production frontend URLs |
| `SENTRY_DSN` | Optional; Sentry only loads if set |

Frontend (build-time): `VITE_API_URL=/api/v1/` when served from the same host.

## Local development (without Docker)

**Backend:**

```bash
cd devangwabackend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # set DEBUG=True, SECRET_KEY for dev
python manage.py migrate
python manage.py runserver
```

**Frontend:**

```bash
cd devangwacoaching
npm install
cp .env.example .env   # VITE_API_URL=http://127.0.0.1:8000/api/v1/
npm run dev
```

## Application flows (implemented)

### Course enrollment

1. User views `GET /api/v1/course/courses/{slug}/`
2. Free course: `POST /api/v1/course/courses/{slug}/enroll/` (empty body)
3. Paid course: checkout calls payments `POST /api/v1/payments/checkout/`, then enroll on success
4. List enrollments: `GET /api/v1/course/courses/enrolled/`

Frontend: `src/services/courseService.js`, checkout in `src/views/pages/shop/checkout/`.

### Authentication

- JWT: `POST /api/v1/auth/jwt/create/`, refresh via `POST /api/v1/auth/jwt/refresh/`
- Register: `POST /api/v1/auth/users/` with `full_name`, `email`, `password`, optional `phonenumber`
- Profile update: `PUT /api/v1/auth/profile/` (multipart supported)

## Deployment readiness

### Backend

| Item | Status |
|------|--------|
| Environment-based settings | Done |
| Production security headers | Done (when `DEBUG=False`) |
| Health endpoints | Done |
| PostgreSQL support | Done |
| Sentry (optional) | Done |
| Course/enrollment API | Done |
| Simulated payments | **Replace before live payments** |
| Published-only course list for anonymous users | Done |

### Frontend

| Item | Status |
|------|--------|
| `courseService.js` API layer | Done |
| Course catalog & detail | Done |
| Checkout & enroll paths | Done |
| Auth store / JWT refresh | Done |
| `VITE_API_URL` configuration | Done |

### Docker / CI

| Item | Status |
|------|--------|
| Monorepo Dockerfile | Done |
| Runtime migrations | Done |
| Nginx + Gunicorn | Done |
| GitHub Actions (test + build) | Done |

### Still recommended for production

1. Replace simulated payment logic in `payments/views.py`
2. TLS certificates on Nginx (Let's Encrypt)
3. Managed PostgreSQL with backups (`backup.sh` for pg_dump)
4. Pin Node/Python versions in CI and Docker
5. Restrict admin URL or use strong admin credentials

## Backup

```bash
./devangwabackend/backup.sh
```

Supports PostgreSQL (`pg_dump`) and SQLite (file copy). Retains the last 7 backups.

## Support checklist

1. `GET /health/` returns `{"status":"ok"}`
2. `python manage.py check` passes
3. `python manage.py test` passes
4. Frontend `npm run lint` passes
5. Verify enroll + checkout on staging with test user
