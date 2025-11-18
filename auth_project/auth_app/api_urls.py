from django.urls import path
from . import api_views

urlpatterns = [
    path('register/', api_views.api_register, name='api_register'),
    path('login/', api_views.api_login, name='api_login'),
    path('logout/', api_views.api_logout, name='api_logout'),
    path('profile/', api_views.api_profile, name='api_profile'),
    path('users/', api_views.api_users_list, name='api_users_list'),
    path('users/<int:pk>/', api_views.api_user_detail, name='api_user_detail'),
]

