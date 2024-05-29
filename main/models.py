
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
class Sitadmin(models.Model):
    codesita = models.CharField(db_column='CODESITA', primary_key=True, max_length=3)  # Field name made lowercase.
    dessita = models.CharField(db_column='DESSITA', max_length=40, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    paye = models.BooleanField(db_column='PAYE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SITADMIN'
    def __str__(self) :
        return self.codesita
class Unite(models.Model):
    codeuni = models.CharField(db_column='CODEUNI', primary_key=True, max_length=3)  # Field name made lowercase.
    desuni = models.CharField(db_column='DESUNI', max_length=30, blank=True, null=True)  # Field name made lowercase.
    type_uni = models.CharField(db_column='TYPE_UNI', max_length=1, blank=True, null=True)  # Field name made lowercase.
    adruni = models.CharField(db_column='ADRUNI', max_length=70, blank=True, null=True)  # Field name made lowercase.
    nssuni = models.CharField(db_column='NSSUNI', max_length=20, blank=True, null=True)  # Field name made lowercase.
    tirg = models.FloatField(db_column='TIRG', blank=True, null=True)  # Field name made lowercase.
    codewil = models.CharField(db_column='CODEWIL', max_length=3, blank=True, null=True)  # Field name made lowercsase.
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
    def __str__(self) :
        return self.codeuni
class Agent(models.Model):
    matricule = models.CharField(db_column='MATAG', primary_key=True, max_length=5)  # Field name made lowercase.
    nom = models.CharField(db_column='NOMAG', max_length=30, blank=True, null=True)  # Field name made lowercase.
    prenom = models.CharField(db_column='PREAG', max_length=25, blank=True, null=True)  # Field name made lowercase.
    unite = models.ForeignKey(Unite,db_column='CODEUNIA',related_name="unite_agent",on_delete=models.CASCADE,null=True,max_length=3, blank=True)
    sex = models.CharField(db_column='SEXAG', max_length=1, blank=True, null=True)  # Field name made lowercase.
    date_de_naissance = models.DateTimeField(db_column='DATENAIS', blank=True, null=True) 
    status = models.ForeignKey(Sitadmin,db_column='SITADMIN',related_name="situation_agent",on_delete=models.SET_NULL,null=True,max_length=3, blank=True)
    dateemb = models.DateTimeField(db_column='DATEEMB', blank=True, null=True)
    codepw = models.CharField(db_column='CODEPW', max_length=6, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'AGENT'
    def __str__(self):
        return self.matricule

import hashlib

class Utilisateur(models.Model):
    matricule = models.OneToOneField(Agent,db_column='utilisateur',related_name="agent_user", primary_key=True, max_length=5,on_delete=models.CASCADE)
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

class PaieHist(models.Model):
    mois = models.CharField(db_column='MOIS', max_length=2, blank=True, null=True)  # Field name made lowercase.
    exercice = models.CharField(db_column='EXERCICE', max_length=4, blank=True, null=True)  # Field name made lowercase.
    datep = models.DateTimeField(db_column='DATEP', blank=True, null=True)  # Field name made lowercase.
    matag = models.CharField(db_column='MATAG', max_length=5, blank=True, null=True)  # Field name made lowercase.
    coderub = models.CharField(db_column='CODERUB', max_length=4, blank=True, null=True)  # Field name made lowercase.
    libeller = models.CharField(db_column='LIBELLER', max_length=100, blank=True, null=True)  # Field name made lowercase.
    base = models.DecimalField(db_column='BASE', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taux = models.FloatField(db_column='TAUX', blank=True, null=True)  # Field name made lowercase.
    retenues = models.DecimalField(db_column='RETENUES', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    gains = models.DecimalField(db_column='GAINS', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    codeunia = models.CharField(db_column='CODEUNIA', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PAIE_HIST'
class Paie(models.Model):
    matag = models.CharField(db_column='MATAG', max_length=5)  # Field name made lowercase.
    coderub = models.CharField(db_column='CODERUB', max_length=4)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    libeller = models.CharField(db_column='LIBELLER', max_length=150, blank=True, null=True)  # Field name made lowercase.
    base = models.DecimalField(db_column='BASE', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    taux = models.FloatField(db_column='TAUX', blank=True, null=True)  # Field name made lowercase.
    retenues = models.DecimalField(db_column='RETENUES', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    gains = models.DecimalField(db_column='GAINS', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    codeunia = models.CharField(db_column='CODEUNIA', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PAIE'
class Postew(models.Model):
    codepos = models.CharField(db_column='CODEPOS', primary_key=True, max_length=6)  # Field name made lowercase.
    despos = models.CharField(db_column='DESPOS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cat = models.CharField(db_column='CAT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    codef = models.CharField(db_column='CODEF', max_length=1, blank=True, null=True)  # Field name made lowercase.
    codesf = models.CharField(db_column='CODESF', max_length=3, blank=True, null=True)  # Field name made lowercase.
    codessf = models.CharField(max_length=4, blank=True, null=True)
    code_interime = models.CharField(max_length=2, blank=True, null=True)
    code_interim = models.CharField(max_length=2, blank=True, null=True)
    rub_a10 = models.BooleanField(db_column='Rub_A10', blank=True, null=True)  # Field name made lowercase.
    nbj_a16 = models.BooleanField(db_column='nbj_A16', blank=True, null=True)  # Field name made lowercase.
    ca = models.BooleanField(blank=True, null=True)
    supprime = models.BooleanField(db_column='SUPPRIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'POSTEW'


class HistAgent(models.Model):
    mois = models.CharField(db_column='MOIS', max_length=2, blank=True, null=True)  # Field name made lowercase.
    exercice = models.CharField(db_column='EXERCICE', max_length=4, blank=True, null=True)  # Field name made lowercase.
    matricule = models.CharField(db_column='MATAG', max_length=5,primary_key=True)  # Field name made lowercase.
    modepaie = models.CharField(db_column='MODEPAIE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    numcompte = models.CharField(db_column='NUMCOMPTE', max_length=25, blank=True, null=True)  # Field name made lowercase.
    sitfam = models.CharField(db_column='SITFAM', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nbenf = models.IntegerField(db_column='NBENF', blank=True, null=True)  # Field name made lowercase.
    statut = models.CharField(db_column='STATUT', max_length=1, blank=True, null=True)  # Field name made lowercase.
    sitadmin = models.CharField(db_column='SITADMIN', max_length=3, blank=True, null=True)  # Field name made lowercase.
    datesita = models.DateTimeField(db_column='DATESITA', blank=True, null=True)  # Field name made lowercase.
    codepwn = models.CharField(db_column='CODEPWN', max_length=6, blank=True, null=True)  # Field name made lowercase.
    code_prof = models.CharField(db_column='CODE_PROF', max_length=2, blank=True, null=True)  # Field name made lowercase.
    typecais = models.CharField(db_column='TYPECAIS', max_length=2, blank=True, null=True)  # Field name made lowercase.
    nbj = models.FloatField(db_column='NBJ', blank=True, null=True)  # Field name made lowercase.
    cat = models.CharField(db_column='CAT', max_length=2, blank=True, null=True)  # Field name made lowercase.
    sec = models.IntegerField(db_column='SEC', blank=True, null=True)  # Field name made lowercase.
    sb = models.DecimalField(db_column='SB', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    saluniq = models.BooleanField(db_column='SALUNIQ', blank=True, null=True)  # Field name made lowercase.
    codemutag = models.BooleanField(db_column='CODEMUTAG', blank=True, null=True)  # Field name made lowercase.
    nummutag = models.CharField(db_column='NUMMUTAG', max_length=8, blank=True, null=True)  # Field name made lowercase.
    codecapdec = models.BooleanField(db_column='CODECAPDEC', blank=True, null=True)  # Field name made lowercase.
    compchir = models.BooleanField(db_column='COMPCHIR', blank=True, null=True)  # Field name made lowercase.
    transveh = models.CharField(db_column='TRANSVEH', max_length=1, blank=True, null=True)  # Field name made lowercase.
    type_c = models.CharField(max_length=1, blank=True, null=True)
    profession = models.CharField(db_column='PROFESSION', max_length=70, blank=True, null=True)  # Field name made lowercase.
    codeunia = models.CharField(db_column='CODEUNIA', max_length=4, blank=True, null=True)  # Field name made lowercase.
    code_dir = models.CharField(max_length=1, blank=True, null=True)
    abbat_irg = models.BooleanField(db_column='ABBAT_IRG', blank=True, null=True)  # Field name made lowercase.
    handic = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'HIST_AGENT'