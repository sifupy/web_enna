
from django.db import models


class Agent(models.Model):
    matricule = models.CharField(primary_key=True, max_length=50)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    date_naissance = models.DateField()
    status = models.CharField(max_length=50)
    unite = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'agent'

import hashlib
import os
class Utilisateur(models.Model):
    matricule = models.CharField(max_length=20, unique=True)  
    mot_de_passe = models.CharField(max_length=128)  
    is_admin = models.BooleanField(default=False) #C'est pour definer le role

    def set_password(self, raw_password):
        salt = os.urandom(16)  
        hashed = hashlib.sha256(salt + raw_password.encode()).hexdigest()  
        self.mot_de_passe = salt.hex() + ':' + hashed  

    def check_password(self, raw_password):
        salt, stored_hash = self.mot_de_passe.split(':')  
        hashed = hashlib.sha256(bytes.fromhex(salt) + raw_password.encode()).hexdigest()  
        return hashed == stored_hash  
