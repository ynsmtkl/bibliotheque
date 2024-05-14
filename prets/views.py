from django.shortcuts import render
from dashboard.models import Livre, PretModel, ListAttente, Stock
from .forms import LivrePretForm
import datetime
from django.conf import settings
from django.core.mail import send_mail


def demandePret(request):
    livres = Livre.objects.all()

    if request.method == "POST":
        myform = LivrePretForm(data=request.POST)

        if myform.is_valid() and request.user.is_authenticated:
            pret_livre = Livre.objects.get(titre=myform.cleaned_data['titre'])

            if PretModel.objects.filter(lecteur=request.user.id, livre=pret_livre.id) or PretModel.objects.filter(
                    lecteur=request.user.id, nbre_prets__gte=3):
                return render(request, "prets/refuser.html")

            if PretModel.objects.filter(lecteur=request.user.id, date_retour__lt=datetime.date.today()):

                return render(request, "prets/refuser-retard.html")

            stock = Stock.objects.get(livre_id=pret_livre.id)
            if stock.quantite > 1 and not pret_livre.hors_pret:
                PretModel.objects.create(livre=pret_livre,
                                         lecteur=request.user,
                                         date_pret=datetime.date.today(),
                                         date_retour=datetime.date.today() + datetime.timedelta(days=30))

                cte = PretModel.objects.filter(lecteur=request.user.id)[0]
                for pret in PretModel.objects.filter(lecteur=request.user.id):
                    pret.nbre_prets = cte.nbre_prets + 1
                    pret.save()

                stock.quantite -= 1
                stock.save()

                return render(request, "prets/approve.html")

            elif stock.quantite == 1:
                ListAttente.objects.create(livre_att=pret_livre, lecteur=request.user,
                                           date_att=datetime.datetime.now())

                return render(request, "prets/enregister-attente.html")

            elif pret_livre.hors_pret:
                return render(request, "prets/hors-pret.html")
        else:
            print('error')

    return render(request, 'prets/demandepret.html', {'livres': livres})


def retourLivre(request):
    livres = PretModel.objects.filter(lecteur=request.user.id)
    if request.method == "POST":
        myform = LivrePretForm(data=request.POST)
        if myform.is_valid() and request.user.is_authenticated:
            pret_livre = Livre.objects.get(titre=myform.cleaned_data['titre'])
            if PretModel.objects.filter(lecteur=request.user.id, date_retour__lt=datetime.date.today()):

                return render(request, "prets/regler-situation.html")
            else:
                livre_retour = Livre.objects.get(pk=pret_livre.id)
                stock = Stock.objects.get(livre_id=livre_retour.id)

                if ListAttente.objects.filter(livre_att=pret_livre.id):
                    lecteur = ListAttente.objects.filter(livre_att=pret_livre.id)[0]
                    subject = 'Livre en attente est désormais disponible'
                    body = f"Bonjour,\n Suite a votre demanade faite le {lecteur.date_att},  le livre {lecteur.livre_att.titre} est désomrais disponible pour le pret " + lecteur.lecteur.username
                    send_mail(subject, body, settings.EMAIL_HOST_USER,
                              [lecteur.lecteur.email])
                    lecteur.delete()

                stock.quantite += 1
                stock.save()
                pret_retour = PretModel.objects.get(livre=livre_retour.id, lecteur=request.user.id)
                pret_retour.delete()

                if PretModel.objects.filter(lecteur=request.user.id):
                    cte = PretModel.objects.filter(lecteur=request.user.id)[0]
                    for pret in PretModel.objects.filter(lecteur=request.user.id):
                        pret.nbre_prets = cte.nbre_prets - 1
                        pret.save()

                return render(request, "prets/livre-retourne.html")

    return render(request, 'prets/retourpret.html', {'livres': livres, 'user': request.user})


def attLivre(request):
    livres = ListAttente.objects.filter(lecteur=request.user.id)
    return render(request, 'prets/attente.html', {'livres': livres, 'user': request.user})
