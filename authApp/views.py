from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .forms import (
    CustomUserCreationForm, 
    LoginForm, 
    PasswordResetRequestForm, 
    PasswordResetConfirmForm
)
from .models import CustomUser
from .utils import send_verification_email, send_password_reset_email

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_verified = False
            user.save()
            
            # Envoi de l'email de vérification
            send_verification_email(request, user)
            
            messages.success(request, 'Compte créé. Vérifiez votre email pour activer votre compte.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'authApp/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Authentification avec l'email
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                if user.is_verified:
                    login(request, user)
                    messages.success(request, 'Connexion réussie.')
                    return redirect('home')  # Remplacer par votre page d'accueil
                else:
                    messages.warning(request, 'Compte non vérifié. Vérifiez votre email.')
            else:
                messages.error(request, 'Identifiants invalides.')
    else:
        form = LoginForm()
    return render(request, 'authApp/login.html', {'form': form})

def verify_email(request, token):
    try:
        user = CustomUser.objects.get(verification_token=token)
        user.verify()
        messages.success(request, 'Votre email a été vérifié. Vous pouvez maintenant vous connecter.')
    except ObjectDoesNotExist:
        messages.error(request, 'Lien de vérification invalide ou expiré.')
    
    return redirect('login')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('login')

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                send_password_reset_email(request, user)
                messages.success(request, 'Un email de réinitialisation a été envoyé.')
                return redirect('login')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Aucun compte associé à cet email.')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'authApp/password_reset_request.html', {'form': form})

def password_reset_confirm(request, token):
    try:
        user = CustomUser.objects.get(password_reset_token=token)
        
        if request.method == 'POST':
            form = PasswordResetConfirmForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password1']
                user.set_password(new_password)
                user.password_reset_token = None
                user.save()
                
                messages.success(request, 'Mot de passe réinitialisé avec succès.')
                return redirect('login')
        else:
            form = PasswordResetConfirmForm()
        
        return render(request, 'authApp/password_reset_confirm.html', {'form': form, 'token': token})
    
    except CustomUser.DoesNotExist:
        messages.error(request, 'Lien de réinitialisation invalide ou expiré.')
        return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'authApp/profile.html', {'user': request.user})
