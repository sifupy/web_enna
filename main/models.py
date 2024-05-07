
from django.db import models


# class Agent(models.Model):
#     matricule = models.CharField(primary_key=True, max_length=50)
#     nom = models.CharField(max_length=50)
#     prenom = models.CharField(max_length=50)
#     date_naissance = models.DateField()
#     status = models.CharField(max_length=50)
#     unite = models.IntegerField()

#     class Meta:
#         managed = False
#         db_table = 'agent'

import hashlib
import os
# class Utilisateur(models.Model):
#     matricule = models.CharField(max_length=20, unique=True)  
#     mot_de_passe = models.CharField(max_length=128)  
#     is_admin = models.BooleanField(default=False) #C'est pour definer le role

#     def set_password(self, raw_password):
#         salt = os.urandom(16)  
#         hashed = hashlib.sha256(salt + raw_password.encode()).hexdigest()  
#         self.mot_de_passe = salt.hex() + ':' + hashed  

#     def check_password(self, raw_password):
#         salt, stored_hash = self.mot_de_passe.split(':')  
#         hashed = hashlib.sha256(bytes.fromhex(salt) + raw_password.encode()).hexdigest()  
#         return hashed == stored_hash  


#############################################################################################################
class Agent(models.Model):
    matricule = models.CharField(db_column='MATAG', primary_key=True, max_length=5)  # Field name made lowercase.
    nom = models.CharField(db_column='NOMAG', max_length=30, blank=True, null=True)  # Field name made lowercase.
    prenom = models.CharField(db_column='PREAG', max_length=25, blank=True, null=True)  # Field name made lowercase.
    unite = models.CharField(db_column='CODEUNIA', max_length=3, blank=True, null=True)
    sex = models.CharField(db_column='SEXAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    date_de_naissance = models.DateTimeField(db_column='DATENAIS', blank=True, null=True) 
    status = models.CharField(db_column='SITADMIN', max_length=3, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'AGENT'
class Unite(models.Model):
    codeuni = models.CharField(db_column='CODEUNI', primary_key=True, max_length=3)  # Field name made lowercase.
    desuni = models.CharField(db_column='DESUNI', max_length=30, blank=True, null=True)  # Field name made lowercase.
    type_uni = models.CharField(db_column='TYPE_UNI', max_length=1, blank=True, null=True)  # Field name made lowercase.
    adruni = models.CharField(db_column='ADRUNI', max_length=70, blank=True, null=True)  # Field name made lowercase.
    nssuni = models.CharField(db_column='NSSUNI', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tirg = models.FloatField(db_column='TIRG', blank=True, null=True)  # Field name made lowercase.
    codewil = models.CharField(db_column='CODEWIL', max_length=3, blank=True, null=True)  # Field name made lowercase.
    unite_cnas = models.CharField(db_column='UNITE_CNAS', max_length=4, blank=True, null=True)  # Field name made lowercase.
    codecnassa = models.CharField(db_column='CODECNASSA', max_length=5, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', max_length=4, blank=True, null=True)  # Field name made lowercase.
    adress_mail = models.CharField(max_length=30, blank=True, null=True)
    libelle_dir = models.CharField(max_length=70, blank=True, null=True)
    tel = models.CharField(max_length=12, blank=True, null=True)
    fax = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'UNITE'
import hashlib

class Utilisateur(models.Model):
    matricule = models.CharField(db_column='utilisateur', primary_key=True, max_length=5)
    mot_de_passe = models.CharField(db_column='Motpasse', max_length=8)  # Truncated hash
    is_admin = models.BooleanField(db_column='ADMIN',default=False)  # Field name made lowercase.
    nom = models.CharField(max_length=25)
    prenom = models.CharField(max_length=25)
    gestion_t = models.BooleanField(db_column='Gestion_t',default=False)  # Field name made lowercase.
    gesst_p = models.BooleanField(default=False)
    edition = models.BooleanField(default=False)
    param = models.BooleanField(db_column='PARAM',default=False)  # Field name made lowercase.
    recherche = models.BooleanField(default=False)
    statistque = models.BooleanField(db_column='Statistque',default=False)  # Field name made lowercase.
    mutation = models.BooleanField(default=False)
    intrerrup = models.BooleanField(default=False)
    calcul_conge = models.BooleanField(default=False)
    presences = models.BooleanField(default=False)
    outils = models.BooleanField(default=False)
    gest_cong = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'user_pers'

    def hash_password_truncated(self, raw_password):
        """
        Generates a truncated hash for the given raw password.
        """
        full_hash = hashlib.sha256(raw_password.encode()).hexdigest()  # Generate full hash
        truncated_hash = full_hash[:8]  # Truncate to 8 characters
        return truncated_hash

    def set_password(self, raw_password):
        """
        Sets the password to a truncated hash.
        """
        truncated_hash = self.hash_password_truncated(raw_password)  # Get truncated hash
        self.mot_de_passe = truncated_hash  # Store truncated hash

    def check_password(self, raw_password):
        """
        Checks if the given raw password matches the stored truncated hash.
        """
        stored_hash = self.mot_de_passe  # Retrieve the stored truncated hash
        user_hash = self.hash_password_truncated(raw_password)  # Hash the given password
        return user_hash == stored_hash  # Check if the hashes match

 