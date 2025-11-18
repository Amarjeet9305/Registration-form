# Registration Form System - Project Report

## 1. Problem Statement

In today's digital age, secure user authentication and registration systems are fundamental requirements for web applications. Traditional registration systems often lack essential features such as email verification, password recovery mechanisms, role-based access control, and modern user interfaces. This project addresses these limitations by developing a comprehensive registration and authentication system using Django framework with the following key requirements:

- Secure user registration and authentication
- Email verification for account activation
- Password reset functionality
- User profile management with photo upload
- Role-based access control (User/Admin)
- RESTful API endpoints for mobile/third-party integration
- Modern, responsive Bootstrap UI
- Admin dashboard for user management

## 2. Objectives

### Primary Objectives:
1. **User Registration**: Implement a secure registration system with email verification
2. **User Authentication**: Create login/logout functionality with role-based access
3. **Password Management**: Develop forgot password and reset password features
4. **User Profile**: Build profile management system with photo upload capability
5. **Role-Based Access**: Implement User and Admin roles with appropriate permissions
6. **REST APIs**: Develop RESTful APIs using Django REST Framework
7. **Admin Dashboard**: Create admin interface to view and manage all registered users
8. **Modern UI**: Design beautiful, responsive forms using Bootstrap 5

### Secondary Objectives:
- Secure password handling using Django's built-in authentication
- Database storage of user data with custom profile model
- Email notification system for verification and password reset
- Token-based authentication for API access
- Comprehensive project documentation

## 3. System Modules

### 3.1 Authentication Module
- **User Registration**: Handles new user signup with validation
- **Email Verification**: Sends verification email and activates account upon verification
- **User Login**: Authenticates users and redirects based on role
- **User Logout**: Securely logs out users
- **Password Reset**: Forgot password and reset password functionality

### 3.2 User Profile Module
- **Profile View**: Display user information and profile details
- **Profile Update**: Edit personal information, phone, and upload profile photo
- **Profile Display**: Show profile photo, role, and verification status

### 3.3 Admin Module
- **Admin Dashboard**: View all registered users with search functionality
- **User Management**: Display user details, roles, verification status
- **User Statistics**: Show total user count and filtered results

### 3.4 API Module
- **Registration API**: REST endpoint for user registration
- **Authentication API**: Login/logout endpoints with token generation
- **Profile API**: Get and update user profile via API
- **User Management API**: Admin endpoints to list and view users

### 3.5 Database Module
- **User Model**: Django's built-in User model extended with profile
- **UserProfile Model**: Custom model storing phone, photo, role, and verification status
- **Relationships**: One-to-one relationship between User and UserProfile

## 4. Entity Relationship Diagram (ERD)

```
┌─────────────────┐
│      User       │
├─────────────────┤
│ id (PK)         │
│ username        │
│ email           │
│ first_name      │
│ last_name       │
│ password        │
│ is_active       │
│ is_staff        │
│ date_joined     │
└────────┬────────┘
         │
         │ 1:1
         │
         ▼
┌─────────────────┐
│  UserProfile    │
├─────────────────┤
│ id (PK)         │
│ user_id (FK)    │───┐
│ phone           │   │
│ photo           │   │
│ role            │   │
│ email_verified  │   │
│ email_verif_    │   │
│   token         │   │
│ created_at      │   │
│ updated_at      │   │
└─────────────────┘   │
                      │
                      │
┌─────────────────┐   │
│  AuthToken      │   │
├─────────────────┤   │
│ key (PK)        │   │
│ user_id (FK)    │───┘
│ created         │
└─────────────────┘
```

### Relationships:
- **User ↔ UserProfile**: One-to-One relationship
  - Each User has exactly one UserProfile
  - UserProfile.user is ForeignKey to User
  
- **User ↔ AuthToken**: One-to-Many relationship
  - Each User can have multiple tokens (though typically one active)
  - Used for API authentication

## 5. UML Diagrams

### 5.1 Use Case Diagram

```
                    ┌─────────────────┐
                    │   Registration  │
                    │     System      │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Regular    │    │    Admin     │    │   System     │
│    User      │    │    User      │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
        │                    │                    │
        │                    │                    │
   ┌────┴────┐         ┌─────┴─────┐        ┌────┴────┐
   │         │         │           │        │        │
Register  Login    View Users   Manage   Send Email  Verify
Profile  Logout    Search Users  Users    Notify     Token
Update   Reset     View Stats            Generate
Profile  Password
```

### 5.2 Class Diagram

```
┌─────────────────────────────────────┐
│            User (Django)            │
├─────────────────────────────────────┤
│ + id: int                            │
│ + username: str                      │
│ + email: str                         │
│ + first_name: str                    │
│ + last_name: str                     │
│ + password: str                      │
│ + is_active: bool                    │
│ + is_staff: bool                     │
│ + date_joined: datetime              │
├─────────────────────────────────────┤
│ + get_full_name()                    │
└──────────────┬──────────────────────┘
               │ 1
               │
               │ 1
               ▼
┌─────────────────────────────────────┐
│          UserProfile                 │
├─────────────────────────────────────┤
│ + id: int                            │
│ + user: User (FK)                    │
│ + phone: str                         │
│ + photo: ImageField                  │
│ + role: str (choices)                 │
│ + email_verified: bool               │
│ + email_verification_token: str      │
│ + created_at: datetime               │
│ + updated_at: datetime               │
├─────────────────────────────────────┤
│ + is_admin: property                 │
│ + __str__()                          │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│         RegisterForm                 │
├─────────────────────────────────────┤
│ + username: CharField                │
│ + email: EmailField                  │
│ + first_name: CharField              │
│ + last_name: CharField               │
│ + phone: CharField                   │
│ + password1: CharField               │
│ + password2: CharField               │
├─────────────────────────────────────┤
│ + save()                             │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│         UserProfileForm             │
├─────────────────────────────────────┤
│ + phone: CharField                   │
│ + photo: ImageField                  │
│ + role: ChoiceField                  │
├─────────────────────────────────────┤
│ + save()                             │
└─────────────────────────────────────┘
```

### 5.3 Sequence Diagram - User Registration

```
User    Browser    Views    Forms    Models    Email    Database
 │         │         │        │        │         │         │
 │────────>│         │        │        │         │         │
 │  POST   │         │        │        │         │         │
 │────────>│         │        │        │         │         │
 │         │────────>│        │        │         │         │
 │         │         │───────>│        │         │         │
 │         │         │ Validate│       │         │         │
 │         │         │<───────│        │         │         │
 │         │         │───────>│        │         │         │
 │         │         │  Save  │        │         │         │
 │         │         │        │───────>│         │         │
 │         │         │        │        │────────>│         │
 │         │         │        │        │<────────│         │
 │         │         │        │<───────│         │         │
 │         │         │<───────│        │         │         │
 │         │         │───────>│        │         │         │
 │         │         │  Send │        │         │         │
 │         │         │  Email│        │         │────────>│
 │         │         │<───────│        │         │<────────│
 │         │<────────│        │        │         │         │
 │<────────│         │        │        │         │         │
```

## 6. Technology Stack

### Backend:
- **Django 4.2.7**: Web framework
- **Django REST Framework**: API development
- **SQLite**: Database (development)
- **Python**: Programming language

### Frontend:
- **Bootstrap 5.3.0**: CSS framework
- **Bootstrap Icons**: Icon library
- **HTML5/CSS3**: Markup and styling
- **JavaScript**: Client-side interactions

### Security:
- **Django Authentication**: Built-in authentication system
- **CSRF Protection**: Cross-site request forgery protection
- **Token Authentication**: API token-based auth
- **Password Hashing**: Secure password storage

## 7. Features Implementation

### 7.1 User Registration
- Form validation for all fields
- Email uniqueness check
- Password strength validation
- Automatic profile creation
- Email verification token generation
- Account activation via email link

### 7.2 Email Verification
- Secure token generation using secrets module
- Email sending with verification link
- Token validation on verification
- Account activation upon successful verification
- User-friendly success/error messages

### 7.3 Password Reset
- Forgot password form with email input
- Reset token generation and storage
- Email notification with reset link
- Secure password reset with token validation
- Password confirmation matching

### 7.4 User Profile
- Profile photo upload with image handling
- Phone number storage
- Role assignment (User/Admin)
- Profile update functionality
- Profile display with photo

### 7.5 Role-Based Access
- User role stored in UserProfile
- Admin dashboard access control
- Role-based redirect after login
- Admin-only API endpoints
- Permission decorators for views

### 7.6 REST APIs
- Registration endpoint (POST /api/register/)
- Login endpoint (POST /api/login/)
- Logout endpoint (POST /api/logout/)
- Profile endpoint (GET/PUT /api/profile/)
- Users list endpoint (GET /api/users/) - Admin only
- User detail endpoint (GET /api/users/{id}/) - Admin only

### 7.7 Admin Dashboard
- List all registered users
- Search functionality (username, email, name)
- Display user details, roles, verification status
- User statistics
- Responsive table layout

## 8. Database Schema

### User Table (Django Built-in)
- id (Primary Key)
- username (Unique)
- email
- first_name
- last_name
- password (Hashed)
- is_active
- is_staff
- is_superuser
- date_joined
- last_login

### UserProfile Table
- id (Primary Key)
- user_id (Foreign Key → User)
- phone (CharField, max_length=15)
- photo (ImageField, upload_to='profile_photos/')
- role (CharField, choices: 'user', 'admin')
- email_verified (BooleanField, default=False)
- email_verification_token (CharField, max_length=100)
- created_at (DateTimeField, auto_now_add)
- updated_at (DateTimeField, auto_now)

## 9. API Documentation

### Base URL: `/api/`

#### 1. Register User
- **Endpoint**: `POST /api/register/`
- **Authentication**: Not required
- **Request Body**:
  ```json
  {
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepass123",
    "phone": "+1234567890"
  }
  ```
- **Response**: 201 Created
  ```json
  {
    "token": "abc123...",
    "user": {...},
    "message": "Registration successful. Please verify your email."
  }
  ```

#### 2. Login
- **Endpoint**: `POST /api/login/`
- **Authentication**: Not required
- **Request Body**:
  ```json
  {
    "username": "john_doe",
    "password": "securepass123"
  }
  ```
- **Response**: 200 OK
  ```json
  {
    "token": "abc123...",
    "user": {...},
    "profile": {...}
  }
  ```

#### 3. Logout
- **Endpoint**: `POST /api/logout/`
- **Authentication**: Required (Token)
- **Response**: 200 OK
  ```json
  {
    "message": "Logged out successfully"
  }
  ```

#### 4. Get/Update Profile
- **Endpoint**: `GET/PUT /api/profile/`
- **Authentication**: Required (Token)
- **Response**: 200 OK
  ```json
  {
    "phone": "+1234567890",
    "photo": "/media/profile_photos/photo.jpg",
    "role": "user",
    "email_verified": true
  }
  ```

#### 5. List Users (Admin Only)
- **Endpoint**: `GET /api/users/?search=john`
- **Authentication**: Required (Token, Admin)
- **Response**: 200 OK
  ```json
  [
    {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      ...
    }
  ]
  ```

## 10. Installation & Setup

### Prerequisites:
- Python 3.8+
- pip
- virtualenv (recommended)

### Steps:

1. **Clone/Navigate to project directory**
   ```bash
   cd auth_project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django djangorestframework pillow
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Web Interface: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - API Base: http://127.0.0.1:8000/api/

## 11. Security Features

1. **Password Security**
   - Passwords are hashed using Django's PBKDF2 algorithm
   - Password validation (minimum length, complexity)
   - Secure password reset tokens

2. **CSRF Protection**
   - All forms include CSRF tokens
   - API uses token authentication

3. **Email Verification**
   - Accounts inactive until email verified
   - Secure token generation for verification

4. **Role-Based Access**
   - Admin-only endpoints protected
   - Permission decorators on views
   - Role-based redirects

5. **SQL Injection Protection**
   - Django ORM prevents SQL injection
   - Parameterized queries

## 12. Future Enhancements

1. **Two-Factor Authentication (2FA)**
2. **Social Media Login (OAuth)**
3. **Activity Logging**
4. **Email Templates with HTML**
5. **Profile Photo Cropping**
6. **Advanced Search Filters**
7. **User Export Functionality**
8. **Email Notification Preferences**
9. **Account Deletion**
10. **API Rate Limiting**

## 13. Conclusion

This Registration Form System provides a comprehensive solution for user authentication and management with modern features including email verification, password reset, role-based access control, and REST API support. The system is built using Django's robust authentication framework, ensuring security and scalability. The Bootstrap-based UI provides a modern, responsive user experience across all devices.

The project successfully implements all required features:
- ✅ User Registration
- ✅ User Login/Logout
- ✅ Email Verification
- ✅ Forgot/Reset Password
- ✅ User Profile Management
- ✅ Role-Based Access (User/Admin)
- ✅ REST APIs
- ✅ Admin Dashboard
- ✅ Bootstrap UI
- ✅ Secure Password Handling
- ✅ Database Storage

---

**Project Developed By**: [Your Name]  
**Date**: 2024  
**Framework**: Django 4.2.7  
**License**: MIT

