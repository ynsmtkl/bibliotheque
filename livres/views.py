from django.shortcuts import render

from dashboard.models import Livre, Stock


def livres(request):
    livres = Livre.objects.all()
    stock = Stock.objects.all()
    livres_et_stock = zip(livres, stock)
    return render(request, 'pages/livres.html', {'livres_et_stock': livres_et_stock})