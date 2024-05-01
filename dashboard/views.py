from django.shortcuts import render

from dashboard.models import Categorie, Pret, Livre, Lecteur
from django.db.models import Count
from django.db.models.functions import ExtractWeekDay, ExtractMonth
from django.shortcuts import render


def dashboard(request):
    categories_with_count = Categorie.objects.annotate(livre_count=Count('livre'))

    categories_with_demand_counts = Categorie.objects.filter(livre__demande__isnull=False).annotate(
        livre_demand_count=Count('livre__demande'))

    data_jours = get_jours()
    data_mois = get_months()

    categories_count = Categorie.objects.count()
    livre_count = Livre.objects.count()
    lecteurs_count = Lecteur.objects.count()
    prets_count = Pret.objects.count()

    context = {
        'categories_count': categories_count,
        'livres_count': livre_count,
        'lecteurs_count': lecteurs_count,
        'prets_count': prets_count,
        'data_mois': data_mois,
        'data_jours': data_jours,
        'category_counts': list(categories_with_count.values('nom', 'livre_count')),
        'livres_demande_counts': list(categories_with_demand_counts.values('nom', 'livre_demand_count'))
    }

    return render(request, 'index.html', context)


def get_months():
    month_map = {
        1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril', 5: 'Mai', 6: 'Juin',
        7: 'Juillet', 8: 'Août', 9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'
    }

    # Récupérer le nombre d'occurrences de chaque mois
    mois_count = Pret.objects.annotate(
        mois=ExtractMonth('date_pret')
    ).values('mois').annotate(
        count=Count('id')
    )

    # Créer un dictionnaire pour stocker les résultats
    resultats = {month_map[mois['mois']]: mois['count'] for mois in mois_count}

    # Remplir les mois qui n'ont pas d'occurrences avec 0
    for i in range(1, 13):
        if month_map[i] not in resultats:
            resultats[month_map[i]] = 0

    # Trier les mois par leur index
    sorted_resultats = {month: resultats[month] for month in sorted(resultats, key=lambda x: list(month_map.keys()).index(
        list(month_map.keys())[list(month_map.values()).index(x)]))}

    return sorted_resultats


def get_jours():
    jour_map = {1: 'Lundi', 2: 'Mardi', 3: 'Mercredi', 4: 'Jeudi', 5: 'Vendredi', 6: 'Samedi', 7: 'Dimanche'}

    # Récupérer le nombre d'occurrences de chaque jour de la semaine
    jours_count = Pret.objects.annotate(
        jour_semaine=ExtractWeekDay('date_pret')
    ).values('jour_semaine').annotate(
        count=Count('id')
    )

    # Créer un dictionnaire pour stocker les résultats
    resultats = {jour_map[jour['jour_semaine']]: jour['count'] for jour in jours_count}

    # Remplir les jours qui n'ont pas d'occurrences avec 0
    for i in range(1, 8):
        if jour_map[i] not in resultats:
            resultats[jour_map[i]] = 0


    # Trier les jours par leur index dans la semaine
    sorted_resultats = {day: resultats[day] for day in sorted(resultats, key=lambda x: list(jour_map.keys()).index(
            list(jour_map.keys())[list(jour_map.values()).index(x)]))}

    return sorted_resultats

