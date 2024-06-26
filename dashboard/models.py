from django.db import models
from django.contrib.auth.models import User


class Categorie(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)

    def __str__(self):
        return self.nom


class Auteur(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)

    def __str__(self):
        return self.nom


class Livre(models.Model):
    id = models.AutoField(primary_key=True)
    ref = models.CharField(max_length=255)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    auteur = models.ForeignKey(Auteur, on_delete=models.CASCADE)
    DatePublication = models.DateField()
    edition = models.CharField(max_length=255)
    hors_pret = models.BooleanField(default=False)

    def __str__(self):
        return self.titre


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    quantite = models.IntegerField()

    def __str__(self):
        return f"{self.livre.titre} - Qté: {self.quantite}"


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Personne(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Lecteur(models.Model):
    id = models.AutoField(primary_key=True)
    personne = models.ForeignKey(Personne, default=None, on_delete=models.CASCADE)
    cne = models.CharField(max_length=100)

    def __str__(self):
        return self.personne.user.first_name + " " + self.personne.user.last_name


class Bibliothecaire(models.Model):
    id = models.AutoField(primary_key=True)
    personne = models.ForeignKey(Personne, default=None, on_delete=models.CASCADE)
    matricule = models.CharField(max_length=100)

    def __str__(self):
        return self.personne.user.first_name + " " + self.personne.user.last_name


class Pret(models.Model):
    id = models.AutoField(primary_key=True)
    lecteur = models.ForeignKey(Lecteur, on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, default=None, on_delete=models.CASCADE)
    date_pret = models.DateField()
    date_retour = models.DateField()

    def __str__(self):
        return self.lecteur.personne.user.first_name + " " \
               + self.lecteur.personne.user.last_name + " Date de prêt " + str(self.date_pret) \
               + " Date de retour " + str(self.date_retour)


class Status(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=30)
    couleur = models.CharField(max_length=20)


class Demande(models.Model):
    id = models.AutoField(primary_key=True)
    lecteur = models.ForeignKey(Lecteur, on_delete=models.CASCADE)
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    def __str__(self):
        return self.lecteur.personne.user.first_name + " " \
               + self.lecteur.personne.user.last_name + " Demande " + self.livre.titre \
               + " (" + self.status.nom + ") "


class ListAttente(models.Model):
    livre_att = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='livre_att')
    lecteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lecteur_att')
    date_att = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.livre_att.titre + ' ' + self.lecteur.username


class PretModel(models.Model):
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='livre_prete')
    lecteur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lecteur')
    date_pret = models.DateField(auto_now=True)
    date_retour = models.DateField()
    nbre_prets = models.IntegerField(default=0)
    retard = models.IntegerField(null=True, blank=True)
    frais_retard = models.FloatField(null=True, blank=True)
    status = models.SlugField()

    def __str__(self):
        return self.livre.titre + ' ' + self.status

