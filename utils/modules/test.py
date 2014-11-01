from os import environ, path
import sys
import json
import sqlite3
import time
from datetime import date as dt, datetime
sys.path.append('/home/pvernier/code/python/elpaso')
environ['DJANGO_SETTINGS_MODULE'] = 'elpaso.settings'

from jobs.models import Contrat
from jobs.models import Month, Year, Week

def create_json2(periode):
    """ """
    # récupérer la liste des types de contrats
    types_contrat = Contrat.objects.values('type')
    types = [{'key': t, 'values': []} for t in types_contrat]

    today = dt.today()
    week_nb = dt(today.year, today.month, today.day).isocalendar()[1]
    first_day = time.asctime(time.strptime('{0} {1} 1'.format(today.year,
                                 week_nb - 1), '%Y %W %w'))
    first_day = datetime.strptime(first_day, "%a %b %d %H:%M:%S %Y")

    result_month = Month.objects.filter(month=today.month, year= 2056)
    result_year = Year.objects.filter(year= 2088)

    result_week = Week.objects.filter(week=week_nb, year= 5654)

    if len(result_month) == 0:
        month_timestamp = time.mktime(dt(today.year, today.month, 1).timetuple()) * 1000
        update_month = Month(month=today.month, year= today.year, month_milsec=month_timestamp)
        update_month.save()

    if len(result_year) == 0:
        year_timestamp = time.mktime(dt(today.year, 1, 1).timetuple()) * 1000
        update_year = Year(year= today.year, year_milsec=year_timestamp)
        update_year.save()

    if len(result_week) == 0:
        week_timestamp = time.mktime(first_day.timetuple()) * 1000
        update_week = Week(year= today.year, week_milsec=week_timestamp, week=week_nb)
        update_week.save()

    # timestamps en milliseconds
    #ts_year = Year.objects.values('year_milsec')
    #ts_month = Month.objects.values_list('month_milsec', 'cdi')
    #ts_week = Week.objects.values('week_milsec')

    # listes de valeurs des ta
    month_cdi = Month.objects.values('cdi')
    month_cdd = Month.objects.values('cdd')
    month_fpt = Month.objects.values('fpt')
    month_stage = Month.objects.values('stage')
    month_appre = Month.objects.values('apprentissage')
    month_vi = Month.objects.values('vi')
    month_these = Month.objects.values('these')
    month_psdoc = Month.objects.values('post_doc')
    month_missi = Month.objects.values('mission')
    month_other = Month.objects.values('autre')

    # parcourir la table de chaque période (cad 3 fois). Faire gaffe aux futures lignes vides (déjà créées)
    #data_cdi = list(zip(ts_month, month_cdi))
    print(ts_month)

    data = [
    {'key': 'CDI',
    'values': []
    },
    {'key': 'CDD',
    'values': []
    },
    {'key': 'stage',
    'values' : []
    }]

    data = [
    {'key': 'CDI',
    'values': [[1398895200, 12], [1401573600, 14 ]]
    },
    {'key': 'CDD',
    'values': [[1398895200, 10], [1401573600, 9 ]]
    },
    {'key': 'stage',
    'values' : [[1398895200, 5], [1401573600, 7 ]]
    }]

    with open('/home/pvernier/code/python/elpaso/static/json/contrats2_' + periode + '.json', 'w') as f:
                        f.write(json.dumps(data))


def create_json(periode):
    '''Méthode qui créé les différentes agrégations (par jour de la
    semaine, semaine de l'année, mois et année) et les sauvegarde dans un
    fichier json'''

    mois = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin',
            'juillet', 'août', 'septembre', 'octobre', 'novembre',
            'décembre']

    if periode == 'day':
        # Les jours de la semaine
        days = []
        for i in range(1, 8):
            annonces_day = Contrat.objects.filter(day_of_week=i)
            days.append(len(annonces_day))

        data = {'days': ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi',
                         'samedi', 'dimanche'], 'numbers': days}
        with open('/home/pvernier/code/python/elpaso/static/json/contrats_days_of_week.json', 'w') as f:
            f.write(json.dumps(data))

    else:
        agreg = []
        if periode != 'week':
            # Pour avoir toutes les combinaisons existantes pour mois
            # et année
            jours_contrats = Contrat.objects.values('date_pub')\
                                            .datetimes('date_pub', periode)

            if periode == 'month':
                for e in jours_contrats:
                    agreg.append(mois[e.month - 1] + ' ' + str(e.year))
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
            # Variable qui me sert à récupérer le max d'annonces pour
            # un type de contrats. Utilisé par d3 pour l'échelle
            # en ordonnée
            max = 0

            for jour in jours_contrats:
                if periode == 'month':
                    annonces = Contrat.objects\
                                      .filter(date_pub__year=jour.year,
                                              date_pub__month=jour.month)\
                                      .values_list()
                elif periode == 'year':
                    annonces = Contrat.objects\
                                      .filter(date_pub__year=jour.year)\
                                      .values_list()

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

                    data = {'max': max, 'types': types, 'legend': agreg}

                    with open('/home/pvernier/code/python/elpaso/static/json/contrats_' + periode + '.json', 'w') as f:
                        f.write(json.dumps(data))

        # Pour agréger par semaine
        elif periode == 'week':
            # Comme DISTINCT n'est pa faisable sur SQLITE je fais comme
            # ci-dessous
            weeks = []
            sel = Contrat.objects.values('date_pub', 'week_number')
            for s in sel:
                t = (s['date_pub'].year, s['week_number'])
                if t not in weeks:
                    weeks.append(t)
                    agreg.append('semaine ' + str(t[1]) + ' de ' +
                                 str(t[0]))

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
                annonces = Contrat.objects\
                                  .filter(date_pub__year=week[0],
                                          week_number=week[1])\
                                  .values_list()

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

                        if types['apprentissage'][list(weeks).index(week)]\
                           > max:
                            max = types['apprentissage'][list(weeks)
                                                         .index(week)]

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

                        if types['post doc'][list(weeks).index(week)]\
                           > max:
                            max = types['post doc'][list(weeks)
                                                    .index(week)]

                    elif annonce[1] == 'mission':
                        types['mission'][list(weeks).index(week)] = \
                        types['mission'][list(weeks).index(week)] + 1

                        if types['mission'][list(weeks).index(week)] > max:
                            max = types['mission'][list(weeks).index(week)]

                    elif annonce[1] == 'autre':
                        types['autre'][list(weeks).index(week)] =\
                        types['autre'][list(weeks).index(week)] + 1

                        if types['autre'][list(weeks).index(week)] > max:
                            max = types['autre'][list(weeks).index(week)]

                    data = {'max': max, 'types': types, 'legend': agreg}

                    with open('/home/pvernier/code/python/elpaso/static/json/contrats_' + periode + '.json', 'w') as f:
                        f.write(json.dumps(data))



def periodizer(li_id, db_cursor):

    # connexion à la BD Django
    db_django = path.abspath('/home/pvernier/code/python/elpaso/elpaso.sqlite')
    conn_django = sqlite3.connect(db_django)
    c_django = conn_django.cursor()

    for offre in li_id:
        db_cursor.execute("SELECT * FROM contrats WHERE id = "
                          + str(offre))
        # Je récupère dans la variable 'contrat' toutes les colonnes de
        # l'objet
        contrat = db_cursor.fetchall()

        # Je récupère la date de l'annonce
        db_cursor.execute("SELECT date_pub FROM georezo WHERE id = "
                          + str(offre))
        date = db_cursor.fetchone()
        date_object = datetime.strptime(date[0], "%a, %d %b %Y \
                                        %H:%M:%S +0200")

        year = date_object.year
        month_number = date_object.month
        # A corriger
        # day_number = date_object[2]
        # week = dt(year, month_number, day_number).isocalendar()[1]
        # first_day = time.strptime("{0} {1} 1".format(year, week), "%Y %W %w") - time.timezone

        c_django.execute('SELECT * FROM jobs_year\
                                          WHERE year = ' + str(year))
        val_types = c_django.fetchall()

        if len(contrat) > 0:
            if contrat[0][1] == 1:
                c_django.execute('UPDATE jobs_year SET cdi = ' +
                                  str(val_types[0][2] + 1) + ' WHERE year = ' +
                                  str(year))

            elif contrat[0][2] == 1:
                c_django.execute('UPDATE jobs_year SET cdd = ' +
                                  str(val_types[0][3] + 1) + ' WHERE year = ' +
                                  str(year))

            elif contrat[0][3] == 1:
                c_django.execute('UPDATE jobs_year SET fpt = ' +
                                  str(val_types[0][4] + 1) + ' WHERE year = ' +
                                  str(year))

            elif contrat[0][4] == 1:
                c_django.execute('UPDATE jobs_year SET stage = ' +
                                  str(val_types[0][5] + 1) + ' WHERE year = ' +
                                  str(year))

            elif contrat[0][5] == 1:
                c_django.execute('UPDATE jobs_year SET apprentissage = ' +
                                  str(val_types[0][6] + 1) + ' WHERE year = ' +
                                  str(year))

            elif contrat[0][6] == 1:
                c_django.execute('UPDATE jobs_year SET vi = ' +
                                  str(val_types[0][7] + 1) + ' WHERE year = ' +
                                  str(year))

            elif contrat[0][7] == 1:
                c_django.execute('UPDATE jobs_year SET these = ' +
                                  str(val_types[0][8] + 1) + ' WHERE year = ' +
                                  str(year))

            elif contrat[0][8] == 1:
                c_django.execute('UPDATE jobs_year SET post_doc = ' +
                                  str(val_types[0][9] + 1) + ' WHERE year = ' +
                                  str(year))

            elif contrat[0][9] == 1:
                c_django.execute('UPDATE jobs_year SET mission = ' +
                                  str(val_types[0][10] + 1) + ' WHERE year = ' +
                                  str(year))

            elif contrat[0][10]:
                c_django.execute('UPDATE jobs_year SET autre = ' +
                                  str(val_types[0][11] + 1) + ' WHERE year = ' +
                                  str(year))

            conn_django.commit()

create_json2('month')

# create_json('year') 
# create_json('month')   
# create_json('week')
# create_json('day')


# db = path.abspath(r"../../elpaso.sqlite")
# conn = sqlite3.connect(db)
# c = conn.cursor()
# # fetching the ID list
# c.execute("SELECT id FROM georezo")
# liste_input = [i[0] for i in c.fetchall()]

# periodizer(liste_input, c)





# dates = Contrat.objects.values('date_pub')

# for t in dates:
#     print(t)
#     # print(t['date_pub'].isocalendar())
#     print(t['date_pub'].month)


