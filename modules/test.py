from os import environ
import sys
import json
sys.path.append('/home/pvernier/code/python/django_projects/elpaso')
environ['DJANGO_SETTINGS_MODULE'] = 'elpaso.settings'
from jobs.models import Contrat


def create_json(periode):

    mois = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet',
            'août', 'septembre', 'octobre', 'novembre', 'décembre']

    if periode == 'day':
        # Les jours de la semaine
        days = []
        for i in range(1, 8):
            annonces_day = Contrat.objects.filter(day_of_week=i)
            days.append(len(annonces_day))

        data = {'days': ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi',
                         'samedi', 'dimanche'], 'numbers': days}
        with open('/home/pvernier/code/python/django_projects/elpaso/static/json/contrats_days_of_week.json', 'w') as f:
            f.write(json.dumps(data))

    else:
        agreg = []
        if periode != 'week':
            # Pour avoir toutes les combinaisons existantes pour mois et année
            jours_contrats = Contrat.objects.values('date_pub').datetimes('date_pub', periode)

            
            if periode == 'month':
                for e in jours_contrats:
                    agreg.append(mois[e.month] + ' ' + str(e.year))
            elif periode == 'year':
                for e in jours_contrats:
                    agreg.append(e.year)
            else:
                pass

            types = {}
            # DISTINCT ne marche pas sur SQLITE
            # Pour avoir tous les types de contrats existants
            types_contrat = Contrat.objects.values('type')
            for t in types_contrat:
                try:
                    types[t['type']] = [0 for i in jours_contrats]
                except:
                    pass
            # Variable qui me sert à récupérer le max d'annonces pour un type
            # de contrats. Utilisé par d3 pour l'échelle en ordonnée
            max = 0

            for jour in jours_contrats:
                if periode == 'month':
                    annonces = Contrat.objects.filter(date_pub__year = jour.year, date_pub__month = jour.month).values_list()
                elif periode == 'year':
                    annonces = Contrat.objects.filter(date_pub__year = jour.year).values_list()

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

                    data = {'max': max, 'types': types, 'legend' : agreg}

                    with open('/home/pvernier/code/python/django_projects/elpaso/static/json/contrats_' + periode + '.json', 'w') as f:
                        f.write(json.dumps(data))

        # Pour agréger par semaine
        elif periode == 'week':
            # Comme DISTINCT n'est pa faisable sur SQLITE je fais comme ci-dessous
            weeks = []
            sel =Contrat.objects.values('date_pub', 'week_number')
            for s in sel:
                t = (s['date_pub'].year, s['week_number'])
                if t not in weeks:
                    weeks.append(t)
                    agreg.append('semaine ' + str(t[1]) + ' de ' + str(t[0]))
            

            types = {}
            # DISTINCT ne marche pas sur SQLITE
            # Pour avoir tous les types de contrats existants
            types_contrat = Contrat.objects.values('type')
            for t in types_contrat:
                try:
                    types[t['type']] = [0 for i in weeks]
                except:
                    pass
            max = 0

            for week in weeks:
                annonces = Contrat.objects.filter(date_pub__year = week[0], week_number = week[1]).values_list()

                for annonce in annonces:
                    if annonce[1] == 'cdi':
                        types['cdi'][list(weeks).index(week)] = types['cdi'][list(weeks).index(week)] + 1

                        if types['cdi'][list(weeks).index(week)] > max:
                            max = types['cdi'][list(weeks).index(week)]

                    elif annonce[1] == 'cdd':
                        types['cdd'][list(weeks).index(week)] = types['cdd'][list(weeks).index(week)] + 1

                        if types['cdd'][list(weeks).index(week)] > max:
                            max = types['cdd'][list(weeks).index(week)]

                    elif annonce[1] == 'fpt':
                        types['fpt'][list(weeks).index(week)] = types['fpt'][list(weeks).index(week)] + 1

                        if types['fpt'][list(weeks).index(week)] > max:
                            max = types['fpt'][list(weeks).index(week)]

                    elif annonce[1] == 'stage':
                        types['stage'][list(weeks).index(week)] = types['stage'][list(weeks).index(week)] + 1

                        if types['stage'][list(weeks).index(week)] > max:
                            max = types['stage'][list(weeks).index(week)]

                    elif annonce[1] == 'apprentissage':
                        types['apprentissage'][list(weeks).index(week)] = types['apprentissage'][list(weeks).index(week)] + 1

                        if types['apprentissage'][list(weeks).index(week)] > max:
                            max = types['apprentissage'][list(weeks).index(week)]

                    elif annonce[1] == 'vi':
                        types['vi'][list(weeks).index(week)] = types['vi'][list(weeks).index(week)] + 1

                        if types['vi'][list(weeks).index(week)] > max:
                            max = types['vi'][list(weeks).index(week)]

                    elif annonce[1] == 'these':
                        types['these'][list(weeks).index(week)] = types['these'][list(weeks).index(week)] + 1

                        if types['these'][list(weeks).index(week)] > max:
                            max = types['these'][list(weeks).index(week)]

                    elif annonce[1] == 'post doc':
                        types['post doc'][list(weeks).index(week)] = types['post doc'][list(weeks).index(week)] + 1

                        if types['post doc'][list(weeks).index(week)] > max:
                            max = types['post doc'][list(weeks).index(week)]

                    elif annonce[1] == 'mission':
                        types['mission'][list(weeks).index(week)] = types['mission'][list(weeks).index(week)] + 1

                        if types['mission'][list(weeks).index(week)] > max:
                            max = types['mission'][list(weeks).index(week)]

                    elif annonce[1] == 'autre':
                        types['autre'][list(weeks).index(week)] = types['autre'][list(weeks).index(week)] + 1

                        if types['autre'][list(weeks).index(week)] > max:
                            max = types['autre'][list(weeks).index(week)]

                    data = {'max': max, 'types': types, 'legend': agreg}

                    with open('/home/pvernier/code/python/django_projects/elpaso/static/json/contrats_' + periode + '.json', 'w') as f:
                        f.write(json.dumps(data))








        


create_json('year') 
create_json('month')   
create_json('week')
create_json('day')

# create_json('month')
# # print('\n')
# # print('\n')
# create_json('year')








# dates = Contrat.objects.values('date_pub')

# for t in dates:
#     print(t)
#     # print(t['date_pub'].isocalendar())
#     print(t['date_pub'].month)


