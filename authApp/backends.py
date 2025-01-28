from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Essayer de trouver l'utilisateur par email
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        
        # Vérifier le mot de passe
        if user.check_password(password):
            return user
        return None
