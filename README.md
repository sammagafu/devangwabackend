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

2. **Build and run with Docker:**
   ```bash
   docker build -t devangwa-app .
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
├── Dockerfile               # Production container configuration
├── nginx.conf              # Nginx reverse proxy config
├── backup.sh               # Database backup script
└── HANDOVER.md            # Deployment documentation
```

## 🛠 Technology Stack

### Backend
- **Framework:** Django 4.2 + Django REST Framework
- **Database:** PostgreSQL (production) / SQLite (development)
- **Authentication:** JWT (djangorestframework-simplejwt)
- **Payments:** Custom payment integration
- **Email:** SMTP with django-mailer
- **Monitoring:** Sentry integration
- **Rate Limiting:** django-ratelimit
- **Caching:** Database-backed cache

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

#### Backend
```bash
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=devangwa_db
DATABASE_USER=db_user
DATABASE_PASSWORD=db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
SENTRY_DSN=your-sentry-dsn
```

#### Frontend
```bash
VITE_API_URL=/api/v1/
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/v1/auth/jwt/create/` - Login
- `POST /api/v1/auth/jwt/refresh/` - Refresh token
- `GET /api/v1/auth/users/me/` - Get current user
- `POST /api/v1/auth/users/` - Register new user

### Core Resources
- **Courses:** `/api/v1/course/courses/`
- **Users:** `/api/v1/auth/`
- **Payments:** `/api/v1/payments/`
- **Community:** `/api/v1/community/`

## 🚀 Deployment

### Production Setup
1. Set up PostgreSQL database
2. Configure environment variables
3. Build Docker image: `docker build -t devangwa-app .`
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

- JWT-based authentication
- Rate limiting on API endpoints
- CORS configuration
- CSRF protection
- Secure password hashing
- Environment-based secrets management

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

### Frontend Tests
```bash
cd devangwacoaching
npm run test
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

- Production-ready Docker containerization
- Rate limiting and security enhancements
- PostgreSQL database support
- Sentry monitoring integration
- Automated CI/CD pipeline
- Comprehensive deployment documentation</content>
<parameter name="filePath">/Users/codexl-008/devangwa/devangwabackend/README.md