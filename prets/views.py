from django.shortcuts import render
from django.http import HttpResponse
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
                html = "<div style='max-width: 800px; margin: auto; padding: 30px; border: 2px solid #ccc; " \
                       "border-radius: 8px; background-color: #ffcccc; font-weight: bold; font-size: 20px;'>Refusé, " \
                       "vous avez déjà emprunté ce livre ou vous avez dépassé le nombre maximum de prêts.</div> "
                return HttpResponse(html)

            if PretModel.objects.filter(lecteur=request.user.id, date_retour__lt=datetime.date.today()):
                html = "<div style='max-width: 800px; margin: auto; padding: 30px; border: 2px solid #ccc; " \
                       "border-radius: 8px; background-color: #ffcccc; font-weight: bold; font-size: 20px;'>Refusé, " \
                       "veuillez régler la situation du retard commise.</div> "
                return HttpResponse(html)

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
                html = "<div style='max-width: 800px; margin: auto; padding: 30px; border: 2px solid #ccc; " \
                       "border-radius: 8px; background-color: #d3f5d3; font-weight: bold; font-size: 20px;'>Demande " \
                       "approuvée</div> "
                return HttpResponse(html)

            elif stock.quantite == 1:
                ListAttente.objects.create(livre_att=pret_livre, lecteur=request.user,
                                           date_att=datetime.datetime.now())
                html = "<div style='max-width: 800px; margin: auto; padding: 30px; border: 2px solid #ccc; " \
                       "border-radius: 8px; background-color: #ffe0b2; font-weight: bold; font-size: 20px;'>Vous êtes " \
                       "enregistré dans la liste d'attente en raison de l'insuffisance du livre demandé.</div> "
                return HttpResponse(html)

            elif pret_livre.hors_pret:
                html = "<div style='max-width: 800px; margin: auto; padding: 30px; border: 2px solid #ccc; " \
                       "border-radius: 8px; background-color: #ffcccc; font-weight: bold; font-size: 20px;'>Désolé, " \
                       "ce livre est hors prêt.</div> "
                return HttpResponse(html)
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
                html = "<html><body>Refusé régler votre situation du retard commis</body></html>"
                return HttpResponse(html)
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

                html = "<html><body>Retour du livre avec succés</body></html>"
                return HttpResponse(html)

    return render(request, 'prets/retourpret.html', {'livres': livres, 'user': request.user})


def attLivre(request):
    livres = ListAttente.objects.filter(lecteur=request.user.id)
    return render(request, 'prets/attente.html', {'livres': livres, 'user': request.user})
