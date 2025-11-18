# Django Registration Form System

A comprehensive user registration and authentication system built with Django, featuring email verification, password reset, role-based access control, and REST API support.

## Features

✅ **User Registration** - Secure registration with validation  
✅ **User Login/Logout** - Authentication with role-based redirect  
✅ **Email Verification** - Account activation via email  
✅ **Forgot Password** - Password reset functionality  
✅ **User Profile** - Profile management with photo upload  
✅ **Role-Based Access** - User and Admin roles  
✅ **REST APIs** - Full API support using Django REST Framework  
✅ **Admin Dashboard** - View and manage all registered users  
✅ **Bootstrap UI** - Modern, responsive design  
✅ **Secure Password Handling** - Django's built-in authentication  

## Quick Start

### Installation

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

4. **Run server**
   ```bash
   python manage.py runserver
   ```

5. **Access the application**
   - Web Interface: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - API Base: http://127.0.0.1:8000/api/

## Project Structure

```
auth_project/
├── auth_app/
│   ├── models.py          # UserProfile model
│   ├── views.py           # View functions
│   ├── forms.py           # Form classes
│   ├── admin.py           # Admin configuration
│   ├── api_views.py       # REST API views
│   ├── serializers.py     # API serializers
│   ├── api_urls.py        # API URL routing
│   └── templates/         # HTML templates
│       ├── base.html
│       └── auth/
│           ├── register.html
│           ├── login.html
│           ├── dashboard.html
│           ├── profile.html
│           ├── forgot_password.html
│           ├── reset_password.html
│           └── admin_dashboard.html
├── auth_project/
│   ├── settings.py        # Django settings
│   ├── urls.py            # URL configuration
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/register/` - Register new user
- `POST /api/login/` - Login user
- `POST /api/logout/` - Logout user

### Profile
- `GET /api/profile/` - Get user profile
- `PUT /api/profile/` - Update user profile

### Admin (Admin only)
- `GET /api/users/` - List all users
- `GET /api/users/{id}/` - Get user details

## Web Routes

- `/` - Home (redirects to login/dashboard)
- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout
- `/dashboard/` - User dashboard
- `/profile/` - User profile
- `/verify-email/<token>/` - Email verification
- `/forgot-password/` - Forgot password
- `/reset-password/<token>/` - Reset password
- `/admin-dashboard/` - Admin dashboard (Admin only)

## Configuration

### Email Settings

For production, update email settings in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

Currently configured for development (console backend).

## User Roles

- **User**: Default role, can access dashboard and profile
- **Admin**: Can access admin dashboard and view all users

## Security Features

- Password hashing with PBKDF2
- CSRF protection on all forms
- Token-based API authentication
- Email verification for account activation
- Secure password reset tokens
- Role-based access control

## Technologies Used

- Django 4.2.7
- Django REST Framework
- Bootstrap 5.3.0
- SQLite (development)
- Python 3.8+

## Documentation

See `PROJECT_REPORT.md` for complete project documentation including:
- Problem statement and objectives
- System modules
- ERD and UML diagrams
- API documentation
- Database schema

## License

MIT License

