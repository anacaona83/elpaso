from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from .models import Contrat, Year, Month, Week, Semantic_Global
from .forms import ContactForm
import json

@csrf_exempt
def stats_home(request):
    last_date = Contrat.objects.values('date_pub')[:1][0]['date_pub'].date
    nb_contrats = Contrat.objects.count()
    first_date = Contrat.objects.values('date_pub')[:1][0]['date_pub'].date
    nb_years = Year.objects.count()
    nb_months = Month.objects.count()
    nb_weeks = Week.objects.count()
    nb_words = Semantic_Global.objects.count()

    return render_to_response('jobs/home.html', {
        'last_offer_pub_date': last_date,
        'nb_contrats': nb_contrats,
        'nb_years': nb_years,
        'nb_months': nb_months,
        'nb_weeks': nb_weeks,
        'first_date': first_date,
        'nb_words': nb_words,
    })


def contrat_json(request):

    toto = Contrat.objects.values('date_pub')

    periode = request.GET['mode_aggreg']
    # print(periode)

    # A voir si distingue les memes numéros de jour pour des mois différents
    jours_contrats = Contrat.objects.values('date_pub').datetimes('date_pub', periode)
    # print(jours_contrats)


    types = {}
    # DISTINCT ne marche pas sur SQLITE
    types_contrat = Contrat.objects.values('type')
    for t in types_contrat:
        try:
            types[t['type']] = [0 for i in jours_contrats]
        except:
            pass
    max = 0
    for jour in jours_contrats:

        if periode == 'month':
            annonces = Contrat.objects.filter(date_pub__year = jour.year,
                                              date_pub__month = jour.month).values_list()
        elif periode == 'year':
            annonces = Contrat.objects.filter(date_pub__year = jour.year).values_list()
        elif periode == 'week':
            annonces = Contrat.objects.filter(date_pub__year = jour.year,
                                              date_pub__month = jour.month,
                                              date_pub__day = jour.day).values_list()
        else:
            continue

        for annonce in annonces:
            if annonce[1] == 'cdi':
                types['cdi'][list(jours_contrats).index(jour)] = types['cdi'][list(jours_contrats).index(jour)] + 1

                if types['cdi'][list(jours_contrats).index(jour)] > max:
                    max = types['cdi'][list(jours_contrats).index(jour)]

            elif annonce[1] == 'cdd':
                types['cdd'][list(jours_contrats).index(jour)] = types['cdd'][list(jours_contrats).index(jour)] + 1

                if types['cdd'][list(jours_contrats).index(jour)] > max:
                    max = types['cdd'][list(jours_contrats).index(jour)]

            elif annonce[1] == 'fpt':
                types['fpt'][list(jours_contrats).index(jour)] = types['fpt'][list(jours_contrats).index(jour)] + 1

                if types['fpt'][list(jours_contrats).index(jour)] > max:
                    max = types['fpt'][list(jours_contrats).index(jour)]

            elif annonce[1] == 'stage':
                types['stage'][list(jours_contrats).index(jour)] = types['stage'][list(jours_contrats).index(jour)] + 1

                if types['stage'][list(jours_contrats).index(jour)] > max:
                    max = types['stage'][list(jours_contrats).index(jour)]

            elif annonce[1] == 'apprentissage':
                types['apprentissage'][list(jours_contrats).index(jour)] = types['apprentissage'][list(jours_contrats).index(jour)] + 1

                if types['apprentissage'][list(jours_contrats).index(jour)] > max:
                    max = types['apprentissage'][list(jours_contrats).index(jour)]

            elif annonce[1] == 'vi':
                types['vi'][list(jours_contrats).index(jour)] = types['vi'][list(jours_contrats).index(jour)] + 1

                if types['vi'][list(jours_contrats).index(jour)] > max:
                    max = types['vi'][list(jours_contrats).index(jour)]

            elif annonce[1] == 'these':
                types['these'][list(jours_contrats).index(jour)] = types['these'][list(jours_contrats).index(jour)] + 1

                if types['these'][list(jours_contrats).index(jour)] > max:
                    max = types['these'][list(jours_contrats).index(jour)]

            elif annonce[1] == 'post doc':
                types['post doc'][list(jours_contrats).index(jour)] = types['post doc'][list(jours_contrats).index(jour)] + 1

                if types['post doc'][list(jours_contrats).index(jour)] > max:
                    max = types['post doc'][list(jours_contrats).index(jour)]

            elif annonce[1] == 'mission':
                types['mission'][list(jours_contrats).index(jour)] = types['mission'][list(jours_contrats).index(jour)] + 1

                if types['mission'][list(jours_contrats).index(jour)] > max:
                    max = types['mission'][list(jours_contrats).index(jour)]

            elif annonce[1] == 'autre':
                types['autre'][list(jours_contrats).index(jour)] = types['autre'][list(jours_contrats).index(jour)] + 1

                if types['autre'][list(jours_contrats).index(jour)] > max:
                    max = types['autre'][list(jours_contrats).index(jour)]

    
    # print(types)
    data = {'max': max, 'types': types}
    # toto = Contrat.objects.values('date_pub')
    # for t in toto:
    #     print(t)
    #     print(t['date_pub'].isocalendar()[1])

    #toto = Contrat.objects.filter(date_pub__day=22).values()
    #print(toto)

    # https://docs.djangoproject.com/en/dev/ref/models/querysets/#dates

     # A LIRE:
     # https://stackoverflow.com/questions/17733495/how-to-group-by-events-by-year-and-month-in-django-orm?lq=1

    return HttpResponse(json.dumps(data), mimetype='application/json')
