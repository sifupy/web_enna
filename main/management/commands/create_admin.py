from django.core.management.base import BaseCommand
from main.models import Utilisateur
from django.core.exceptions import ValidationError

class Command(BaseCommand):
    help = 'Creates an admin user with a specific matricule and password'

    def add_arguments(self, parser):
        parser.add_argument('matricule', type=str, help='Matricule for the admin user')
        parser.add_argument('password', type=str, help='Password for the admin user')

    def handle(self, *args, **kwargs):
        matricule = kwargs['matricule']
        password = kwargs['password']

        # Check if the user already exists
        if Utilisateur.objects.filter(matricule=matricule).exists():
            self.stdout.write(self.style.ERROR(f"User with matricule '{matricule}' already exists"))
            return

        try:
            admin_user = Utilisateur(matricule=matricule)
            admin_user.set_password(password)  # Hash and set the password
            admin_user.is_admin = True  # Mark as admin
            admin_user.save()  # Save the new admin user
            self.stdout.write(self.style.SUCCESS(f"Admin user '{matricule}' created successfully"))
        except Exception as e:  # Handle unexpected errors
            self.stdout.write(self.style.ERROR(f"Error creating admin user: {e}"))
