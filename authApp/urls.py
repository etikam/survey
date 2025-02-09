from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('verify/<str:token>/', views.verify_email, name='verify_email'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('reset-password/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('profile/', views.profile_view, name='profile'),
]
