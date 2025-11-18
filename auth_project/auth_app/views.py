from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.db.models import Q
from .forms import RegisterForm, UserProfileForm, UserUpdateForm
from .models import UserProfile
import secrets

def is_admin(user):
    """Check if user is admin"""
    if not user.is_authenticated:
        return False
    return user.profile.role == 'admin' or user.is_staff

def home(request):
    """Home page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

def register_user(request):
    """User registration with email verification"""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Save user - UserCreationForm handles password hashing when commit=True
            user = form.save()
            
            # Update user fields
            user.is_active = getattr(settings, 'SKIP_EMAIL_VERIFICATION', False)
            user.save()
            
            # Get or create user profile (should be created by signal, but ensure it exists)
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.phone = form.cleaned_data['phone']
            
            # If skipping email verification, mark as verified
            if getattr(settings, 'SKIP_EMAIL_VERIFICATION', False):
                profile.email_verified = True
                profile.email_verification_token = None
                messages.success(request, "Registration Successful! You can now login.")
            else:
                # Generate verification token
                profile.email_verification_token = secrets.token_urlsafe(32)
                # Send verification email
                verification_url = request.build_absolute_uri(
                    f'/verify-email/{profile.email_verification_token}/'
                )
                send_mail(
                    'Verify Your Email - Registration Form',
                    f'Please click the following link to verify your email: {verification_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, "Registration Successful! Please check your email to verify your account.")
            
            profile.save()
            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request, "auth/register.html", {"form": form})

def verify_email(request, token):
    """Verify user email"""
    try:
        profile = UserProfile.objects.get(email_verification_token=token)
        if not profile.email_verified:
            profile.email_verified = True
            profile.email_verification_token = None
            profile.save()
            profile.user.is_active = True
            profile.user.save()
            messages.success(request, "Email verified successfully! You can now login.")
        else:
            messages.info(request, "Email already verified.")
    except UserProfile.DoesNotExist:
        messages.error(request, "Invalid verification token.")
    
    return redirect('login')

def login_user(request):
    """User login with role-based redirect"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            # Check if profile exists, if not create it
            if not hasattr(user, 'profile'):
                UserProfile.objects.create(user=user)
            
            # Allow login if active, or if skipping email verification in development
            skip_verification = getattr(settings, 'SKIP_EMAIL_VERIFICATION', False)
            if user.is_active or (skip_verification and not user.is_superuser):
                login(request, user)
                # Redirect based on role
                if user.profile.role == 'admin' or user.is_staff:
                    return redirect("admin_dashboard")
                return redirect("dashboard")
            else:
                messages.error(request, "Please verify your email before logging in. Check your email for the verification link.")
        else:
            messages.error(request, "Invalid username or password. Please check your credentials and try again.")
    
    return render(request, "auth/login.html")

@login_required
def logout_user(request):
    """User logout"""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")

@login_required
def dashboard(request):
    """User dashboard"""
    return render(request, "auth/dashboard.html", {
        'user': request.user,
        'profile': request.user.profile
    })

@login_required
def profile(request):
    """User profile view and update"""
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    
    return render(request, "auth/profile.html", {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': request.user.profile
    })

def forgot_password(request):
    """Forgot password - send reset link"""
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            # Generate reset token
            token = secrets.token_urlsafe(32)
            user.profile.email_verification_token = token
            user.profile.save()
            
            # Send reset email
            reset_url = request.build_absolute_uri(f'/reset-password/{token}/')
            send_mail(
                'Password Reset Request',
                f'Click the following link to reset your password: {reset_url}\n\nIf you did not request this, please ignore this email.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            messages.success(request, "Password reset link has been sent to your email.")
        except User.DoesNotExist:
            messages.error(request, "No account found with this email address.")
    
    return render(request, "auth/forgot_password.html")

def reset_password(request, token):
    """Reset password with token"""
    try:
        profile = UserProfile.objects.get(email_verification_token=token)
        if request.method == "POST":
            password = request.POST.get("password")
            password_confirm = request.POST.get("password_confirm")
            
            if password == password_confirm and len(password) >= 8:
                profile.user.set_password(password)
                profile.user.save()
                profile.email_verification_token = None
                profile.save()
                messages.success(request, "Password reset successfully! You can now login.")
                return redirect('login')
            else:
                messages.error(request, "Passwords do not match or are too short (minimum 8 characters).")
    except UserProfile.DoesNotExist:
        messages.error(request, "Invalid or expired reset token.")
        return redirect('forgot_password')
    
    return render(request, "auth/reset_password.html")

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard to view all users"""
    search_query = request.GET.get('search', '')
    users = User.objects.all().select_related('profile')
    
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    # Add profile data
    users_data = []
    for user in users:
        users_data.append({
            'user': user,
            'profile': user.profile if hasattr(user, 'profile') else None
        })
    
    return render(request, "auth/admin_dashboard.html", {
        'users_data': users_data,
        'search_query': search_query,
        'total_users': User.objects.count()
    })
