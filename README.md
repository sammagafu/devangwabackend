# Devangwa Coaching Platform

A comprehensive e-learning platform built with Django REST Framework (backend) and Vue.js (frontend), designed for coaching institutions to deliver online courses, manage students, and handle payments.

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### Local Development Setup

1. **Clone the repositories:**
   ```bash
   git clone https://github.com/sammagafu/devangwacoaching.git
   cd devangwacoaching
   ```

2. **Build and run with Docker** (from monorepo root):
   ```bash
   docker build -f devangwabackend/Dockerfile -t devangwa-app .
   docker run -p 80:80 \
     -e DEBUG=True \
     -e ALLOWED_HOSTS=localhost,127.0.0.1 \
     -e SECRET_KEY=your-development-secret-key \
     -e DATABASE_ENGINE=django.db.backends.sqlite3 \
     -e DATABASE_NAME=db.sqlite3 \
     devangwa-app
   ```

3. **Access the application:**
   - Frontend: http://localhost
   - API: http://localhost/api/v1/
   - Health: http://localhost/health/
   - Admin: http://localhost/api/v1/admin/

## 📁 Project Structure

```
devangwa/
├── devangwabackend/          # Django REST API Backend
│   ├── accounts/             # User management & authentication
│   ├── course/               # Course management system
│   ├── coaching/             # Coaching sessions & events
│   ├── community/            # Discussion forums
│   ├── payments/             # Payment processing
│   ├── dashboard/            # Analytics & reporting
│   └── devangwa/             # Django project settings
├── devangwacoaching/         # Vue.js Frontend Application
│   ├── src/
│   │   ├── components/       # Reusable Vue components
│   │   ├── views/           # Page components
│   │   ├── stores/          # Pinia state management
│   │   ├── services/        # API service layer
│   │   └── router/          # Vue Router configuration
│   └── public/              # Static assets
├── Dockerfile               # Build from repo root: -f devangwabackend/Dockerfile
├── docker-entrypoint.sh     # migrate + collectstatic on container start
├── nginx.conf               # Nginx reverse proxy config
├── .env.example             # Environment variable template
├── backup.sh                # Database backup script
├── HANDOVER.md              # Deployment documentation
└── INTEGRATION_GUIDE.md     # API integration for developers
```

## 🛠 Technology Stack

### Backend
- **Framework:** Django 4.2 + Django REST Framework
- **Database:** PostgreSQL (production) / SQLite (development)
- **Authentication:** JWT (djangorestframework-simplejwt)
- **Payments:** Custom payment integration
- **Email:** SMTP with django-mailer
- **Monitoring:** Sentry integration
- **Rate Limiting:** DRF throttling + payment endpoint limits
- **Caching:** LocMem (dev) or configurable via `CACHE_BACKEND`

### Frontend
- **Framework:** Vue.js 3 + Composition API
- **Build Tool:** Vite
- **State Management:** Pinia
- **Routing:** Vue Router 4
- **UI Framework:** Bootstrap 5 + Bootstrap Vue Next
- **HTTP Client:** Axios
- **Icons:** FontAwesome + Oh Vue Icons

### DevOps
- **Containerization:** Docker
- **Web Server:** Nginx (reverse proxy)
- **WSGI Server:** Gunicorn
- **CI/CD:** GitHub Actions
- **Version Control:** Git

## 🔧 Configuration

### Environment Variables

Copy and edit the example files:

- Backend: `cp devangwabackend/.env.example devangwabackend/.env`
- Frontend: `cp devangwacoaching/.env.example devangwacoaching/.env`

See `.env.example` in each project for the full list. Important production variables:

| Variable | Purpose |
|----------|---------|
| `SECRET_KEY` | Required when `DEBUG=False` |
| `PAYMENTS_API_BASE_URL` | Base URL for internal checkout calls (e.g. `https://yourdomain.com/api/v1/payments`) |
| `CORS_ALLOWED_ORIGINS` | Comma-separated frontend origins |
| `SENTRY_DSN` | Optional error monitoring |
| `VITE_API_URL` | Frontend API prefix (`/api/v1/` or full URL) |

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/v1/auth/jwt/create/` - Login
- `POST /api/v1/auth/jwt/refresh/` - Refresh token
- `GET /api/v1/auth/users/me/` - Get current user
- `POST /api/v1/auth/users/` - Register new user

### Core Resources
- **Courses:** `/api/v1/course/courses/` — list, detail, enroll, enrolled
- **Auth:** `/api/v1/auth/` — JWT, users, profile
- **Payments:** `/api/v1/payments/checkout/`
- **Events:** `/api/v1/coaching/events/`
- **Community:** `/api/v1/community/`
- **Health:** `/health/` and `/api/v1/health/`

Full reference: [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)

## 🚀 Deployment

### Production Setup
1. Set up PostgreSQL database
2. Configure environment variables
3. Build Docker image: `docker build -f devangwabackend/Dockerfile -t devangwa-app .` (from monorepo root)
4. Run container with production environment variables
5. Set up SSL certificates (Let's Encrypt recommended)
6. Configure domain and DNS

### Backup Strategy
- Database backups run via `backup.sh` script
- Supports both PostgreSQL and SQLite
- Automated retention of last 7 backups

## 👥 User Roles

1. **Students:** Access courses, make payments, participate in community
2. **Instructors:** Create and manage courses, view analytics
3. **Administrators:** Full system access, user management

## 🔒 Security Features

- JWT authentication with configurable token lifetimes
- Default API permission: authenticated (public read on courses via view permissions)
- Production requires non-default `SECRET_KEY` when `DEBUG=False`
- HTTPS/HSTS/cookie flags when not in debug mode
- CORS and CSRF trusted origins from environment
- DRF rate throttling (anon/user) and payment checkout limits
- Optional Sentry (only loads when `SENTRY_DSN` is set)

## 📊 Monitoring & Analytics

- **Error Tracking:** Sentry integration
- **Performance:** Built-in Django logging
- **Analytics:** Dashboard module for insights
- **Health Checks:** Database connectivity monitoring

## 🧪 Testing

### Backend Tests
```bash
cd devangwabackend
python manage.py test
```

### Frontend Lint
```bash
cd devangwacoaching
npm run lint
```

### CI/CD
- Automated testing on push/PR via GitHub Actions
- Docker image building and validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is proprietary software. All rights reserved.

## 📞 Support

For technical support or questions:
- Check the HANDOVER.md for detailed deployment instructions
- Review API documentation in code comments
- Check GitHub Issues for known problems

## 🔄 Recent Updates

- Aligned course serializers with database models (modules, lectures, tags, reviews)
- Course enrollment: `POST /api/v1/course/courses/{slug}/enroll/`, `GET .../enrolled/`
- Frontend `courseService.js` and fixed checkout/auth/course display flows
- Production settings: conditional Sentry, security headers, health endpoints
- Docker entrypoint for migrations at runtime; build from monorepo root
- `.env.example` files for backend and frontend</content>
<parameter name="filePath">/Users/codexl-008/devangwa/devangwabackend/README.md