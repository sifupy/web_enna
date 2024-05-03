# In auth_backends.py
from .models import Utilisateur
class CustomAuthenticationBackend:
    def authenticate(self, request, matricule=None, password=None):
        try:
            user = Utilisateur.objects.get(matricule=matricule)  # Find user by unique field
            if user.check_password(password):  # Verify password with custom logic
                return user  # Return the authenticated user
        except Utilisateur.DoesNotExist:
            return None  # Return None if authentication fails
    
    def get_user(self, user_id):
        try:
            return Utilisateur.objects.get(pk=user_id)  # Retrieve user by primary key
        except Utilisateur.DoesNotExist:
            return None  # Return None if user doesn't exist
