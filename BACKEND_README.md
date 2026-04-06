# Devangwa Backend - Django REST API

The backend API for the Devangwa Coaching platform, built with Django REST Framework. Provides comprehensive course management, user authentication, payment processing, and community features.

## 🚀 Features

- **User Management:** Registration, authentication, profile management
- **Course System:** Create, manage, and deliver online courses
- **Payment Integration:** Secure payment processing for course purchases
- **Community Features:** Discussion forums and user interactions
- **Analytics Dashboard:** Instructor and admin analytics
- **Email Notifications:** Automated email notifications for various events
- **Rate Limiting:** API protection against abuse
- **Monitoring:** Sentry integration for error tracking

## 🛠 Tech Stack

- **Framework:** Django 4.2.15
- **API Framework:** Django REST Framework 3.15.2
- **Authentication:** JWT (djangorestframework-simplejwt)
- **Database:** PostgreSQL (production) / SQLite (development)
- **Email:** SMTP with django-mailer
- **Rate Limiting:** django-ratelimit
- **Monitoring:** Sentry SDK
- **Payments:** Custom payment gateway integration

## 📁 Project Structure

```
devangwabackend/
├── accounts/                 # User authentication & profiles
│   ├── models.py            # CustomUser, UserDetails models
│   ├── views.py             # Profile management API
│   ├── serializers.py       # User serialization
│   ├── urls.py              # Authentication routes
│   └── tests.py             # User-related tests
├── course/                   # Course management system
│   ├── models.py            # Course, Module, Video, Quiz models
│   ├── views.py             # Course CRUD operations
│   ├── serializers.py       # Course data serialization
│   └── urls.py              # Course API routes
├── coaching/                 # Coaching sessions & events
│   ├── models.py            # Event, Participant models
│   ├── views.py             # Event management
│   └── serializers.py       # Event serialization
├── community/                # Discussion forums
│   ├── models.py            # Thread, Reply models
│   ├── views.py             # Forum operations
│   └── serializers.py       # Forum data handling
├── payments/                 # Payment processing
│   ├── models.py            # Payment, Transaction models
│   ├── views.py             # Payment API endpoints
│   └── serializers.py       # Payment serialization
├── dashboard/                # Analytics & reporting
│   ├── models.py            # Analytics models
│   ├── views.py             # Dashboard data APIs
│   └── serializers.py       # Analytics serialization
├── devangwa/                 # Django project configuration
│   ├── settings.py          # Project settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
├── requirements.txt          # Python dependencies
├── manage.py                # Django management script
└── db.sqlite3               # Development database
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL (recommended for production)

### Installation

1. **Clone and setup:**
   ```bash
   git clone https://github.com/sammagafu/devangwacoaching.git
   cd devangwacoaching/devangwabackend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup:**
   ```bash
   cp .env.example .env  # Create your .env file
   # Edit .env with your configuration
   ```

5. **Database setup:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run development server:**
   ```bash
   python manage.py runserver
   ```

## ⚙️ Configuration

### Environment Variables

```bash
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=devangwa_db
DATABASE_USER=db_user
DATABASE_PASSWORD=db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# External Services
SENTRY_DSN=your-sentry-dsn
PAYMENTS_API_BASE_URL=http://localhost:8000
```

### Key Settings

- **CORS:** Configured for frontend integration
- **JWT:** Access tokens (1 day), Refresh tokens (7 days)
- **Rate Limiting:** Database-backed caching
- **Static Files:** Served via Nginx in production
- **Media Files:** User-uploaded content handling

## 📚 API Endpoints

### Authentication (`/api/v1/auth/`)
- `POST /jwt/create/` - User login
- `POST /jwt/refresh/` - Refresh access token
- `GET /users/me/` - Current user profile
- `POST /users/` - User registration
- `PUT /profile/` - Update user profile

### Courses (`/api/v1/course/`)
- `GET /courses/` - List courses
- `POST /courses/` - Create course (instructors only)
- `GET /courses/{slug}/` - Course details
- `PUT /courses/{slug}/` - Update course
- `GET /modules/` - Course modules
- `GET /videos/` - Course videos

### Payments (`/api/v1/payments/`)
- `POST /process-payment/` - Process course payment
- `GET /payment-history/` - User payment history

### Community (`/api/v1/community/`)
- `GET /threads/` - Discussion threads
- `POST /threads/` - Create thread
- `GET /threads/{id}/replies/` - Thread replies

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### Test Coverage
- User authentication and registration
- Course CRUD operations
- Payment processing
- API permissions and security

## 🔒 Security

### Authentication & Authorization
- JWT-based authentication
- Role-based permissions (Student, Instructor, Admin)
- CSRF protection
- Secure password hashing

### API Security
- Rate limiting on all endpoints
- Input validation and sanitization
- CORS configuration
- SQL injection prevention

### Data Protection
- Environment-based secrets
- Secure database connections
- File upload validation
- Audit logging

## 📊 Monitoring

### Sentry Integration
- Error tracking and reporting
- Performance monitoring
- Release tracking

### Logging
- Django logging configuration
- Request/response logging
- Error logging with context

## 🚀 Deployment

### Docker Deployment
```bash
# Build image
docker build -t devangwa-backend .

# Run container
docker run -p 8000:8000 \
  -e DEBUG=False \
  -e SECRET_KEY=prod-secret \
  -e DATABASE_ENGINE=django.db.backends.postgresql \
  # ... other env vars
  devangwa-backend
```

### Production Checklist
- [ ] DEBUG = False
- [ ] SECRET_KEY from environment
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS enabled
- [ ] Database migrations run
- [ ] Static files collected
- [ ] Admin URL changed
- [ ] Sentry configured

## 🔧 Development

### Code Style
- Black for code formatting
- isort for import sorting
- flake8 for linting

### Database Management
```bash
# Create migrations
python manage.py makemigrations

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### API Documentation
- Interactive API docs available at `/api/docs/` (if configured)
- Postman collection available in `/docs/`

## 🤝 API Integration

### Frontend Integration
The backend provides RESTful APIs consumed by the Vue.js frontend:
- Base URL: `/api/v1/`
- Authentication: JWT Bearer tokens
- Content-Type: `application/json`
- CORS enabled for frontend domain

### Third-party Integrations
- Payment Gateway: Custom integration
- Email Service: SMTP configuration
- Monitoring: Sentry SDK
- File Storage: Local filesystem (configurable)

## 📞 Support

For backend-specific issues:
1. Check Django logs
2. Review API error responses
3. Test with Postman/curl
4. Check database connectivity
5. Verify environment configuration

## 📈 Performance

### Optimization Features
- Database indexing on key fields
- Query optimization with select_related/prefetch_related
- Caching for rate limiting
- Static file optimization
- Database connection pooling

### Monitoring Metrics
- Response times
- Error rates
- Database query performance
- Cache hit rates</content>
<parameter name="filePath">/Users/codexl-008/devangwa/devangwabackend/BACKEND_README.md