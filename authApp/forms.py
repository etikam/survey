from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.validators import RegexValidator
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Numéro de téléphone invalide.')],
        required=False,
        help_text='Numéro de téléphone optionnel (format international)'
    )
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'phone_number', 'password1', 'password2')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'phone_number', 'profile_picture')

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)
    password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label='Adresse email', max_length=254)

class PasswordResetConfirmForm(forms.Form):
    new_password1 = forms.CharField(
        label='Nouveau mot de passe',
        widget=forms.PasswordInput,
        help_text='Entrez un mot de passe sécurisé'
    )
    new_password2 = forms.CharField(
        label='Confirmez le mot de passe',
        widget=forms.PasswordInput,
        help_text='Répétez votre nouveau mot de passe'
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Les mots de passe ne correspondent pas.')
        return cleaned_data
