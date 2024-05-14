from django.core.management import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import datetime

from dashboard.models import PretModel


# cette class est utiliser pour envoyer un mail a clien sur le retard et les frais de cette retard
class Command(BaseCommand):
    def handle(self, **options):
        today = datetime.date.today()
        
        for pret in PretModel.objects.filter(date_retour__lt=today):
            print(pret.lecteur.email)
            print(pret.date_retour)
            pret.retard = (today -pret.date_retour).days
            pret.frais_retard = pret.retard * 5
            subject = 'Retard de la remise du livre prété'
            body = f"Bonjour, un retard de {pret.retard} jr a été comis de votre part au niveau de la remise du livre preté.\n A cet effet , je le regret de vous infomer qu'une pénalité de {pret.frais_retard} dh doit etre payé lors de la remise du livre. \n Veuillez régler votre situation "+ pret.lecteur.username
            send_mail(subject, body, settings.EMAIL_HOST_USER,
                      [pret.lecteur.email])
          
