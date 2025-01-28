import secrets
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def generate_verification_token():
    """Génère un token unique pour la vérification d'email."""
    return secrets.token_urlsafe(32)

def send_verification_email(request, user):
    """
    Envoie un email de vérification à l'utilisateur.
    
    Args:
        request: L'objet requête HTTP
        user: L'instance de l'utilisateur
    """
    # Générer un token de vérification
    verification_token = generate_verification_token()
    
    # Stocker le token dans le modèle utilisateur (à implémenter)
    user.verification_token = verification_token
    user.save()
    
    # Construire l'URL de vérification
    verification_url = request.build_absolute_uri(
        reverse('verify_email', kwargs={'token': verification_token})
    )
    
    # Préparer le contexte pour le template d'email
    email_context = {
        'username': user.username,
        'verification_url': verification_url,
    }
    
    # Rendre le template HTML
    html_message = render_to_string('authApp/verification_email.html', email_context)
    plain_message = strip_tags(html_message)
    
    # Envoyer l'email
    send_mail(
        'Vérifiez votre compte',
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )

def send_password_reset_email(request, user):
    """
    Envoie un email de réinitialisation de mot de passe.
    
    Args:
        request: L'objet requête HTTP
        user: L'instance de l'utilisateur
    """
    # Générer un token de réinitialisation
    reset_token = generate_verification_token()
    
    # Stocker le token dans le modèle utilisateur (à implémenter)
    user.password_reset_token = reset_token
    user.save()
    
    # Construire l'URL de réinitialisation
    reset_url = request.build_absolute_uri(
        reverse('password_reset_confirm', kwargs={'token': reset_token})
    )
    
    # Préparer le contexte pour le template d'email
    email_context = {
        'username': user.username,
        'reset_url': reset_url,
    }
    
    # Rendre le template HTML
    html_message = render_to_string('authApp/password_reset_email.html', email_context)
    plain_message = strip_tags(html_message)
    
    # Envoyer l'email
    send_mail(
        'Réinitialisation de mot de passe',
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )
