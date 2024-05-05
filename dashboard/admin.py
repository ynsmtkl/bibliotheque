from django.contrib import admin

from dashboard.models import *

# Register your models here.
admin.site.register(Personne)
admin.site.register(Lecteur)
admin.site.register(Bibliothecaire)
admin.site.register(Stock)
admin.site.register(Categorie)
admin.site.register(Livre)
admin.site.register(Pret)
admin.site.register(Demande)
admin.site.register(ListAttente)
admin.site.register(PretModel)

