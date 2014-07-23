from os import path, environ
import sys
import sqlite3
import json
from datetime import datetime
from . import LogGuy

sys.path.append('/home/pvernier/code/python/elpaso')
environ['DJANGO_SETTINGS_MODULE'] = 'elpaso.settings'
from jobs.models import Contrat

# logger object
logger = LogGuy.Logyk()


class Fillin():
    def __init__(self, liste_identifiants_offre):
        '''liste_identifiants_offre = liste des ID des nouvelles offres'''
        # connexion à la BD EL Paso
        db = path.abspath('/home/pvernier/code/python/elpaso/elpaso.sqlite')
        self.conn = sqlite3.connect(db)
        self.c = self.conn.cursor()

        # connexion à la BD Django
        db_django = path.abspath('/home/pvernier/code/python/elpaso/db.sqlite3')
        self.conn_django = sqlite3.connect(db_django)
        self.c_django = self.conn_django.cursor()

        # Remplissage des contrats dans la BD django
        logger.append("\tFill in contrats in the Django DB")
        self.contrats(liste_identifiants_offre, self.c)

        logger.append("\tCreate JSON files")
        self.create_json('year')
        self.create_json('month')
        self.create_json('week')
        self.create_json('day')

    def contrats(self, li_id, db_cursor):
        """Méthode qui remplit la table du modele à partir de la table
        initiale"""

        # TO DO :
        # Faire une requete sur la table lieux
        # et remplir les 2 champs du model django qui correspondent

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

            if len(contrat) > 0:
                if contrat[0][1] == 1:
                    type_contrat = 'CDI'

                elif contrat[0][2] == 1:
                    type_contrat = 'CDD'

                elif contrat[0][3] == 1:
                    print(str(offre))
                    type_contrat = 'FPT'

                elif contrat[0][4] == 1:
                    print(str(offre))
                    type_contrat = 'Stage'

                elif contrat[0][5] == 1:
                    print(str(offre))
                    type_contrat = 'Apprentissage'

                elif contrat[0][6] == 1:
                    print(str(offre))
                    type_contrat = 'VI'

                elif contrat[0][7] == 1:
                    print(str(offre))
                    type_contrat = 'Thèse'

                elif contrat[0][8] == 1:
                    print(str(offre))
                    type_contrat = 'Post doc'

                elif contrat[0][9] == 1:
                    print(str(offre))
                    type_contrat = 'Mission'

                elif contrat[0][10]:
                    type_contrat = 'Autre'

                # etc ...
                self.c_django.execute('INSERT INTO jobs_contrat VALUES \
                                      (?,?,?,?,?)', (str(offre),
                                      type_contrat, date_object,
                                      date_object.isocalendar()[1],
                                      date_object.isocalendar()[2]))

                self.conn_django.commit()

    def create_json(self, periode):
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
                        if annonce[1] == 'CDI':
                            types['CDI'][list(jours_contrats).index(jour)] = types['CDI'][list(jours_contrats).index(jour)] + 1

                            if types['CDI'][list(jours_contrats).index(jour)] > max:
                                max = types['CDI'][list(jours_contrats).index(jour)]

                        elif annonce[1] == 'CDD':
                            types['CDD'][list(jours_contrats).index(jour)] = types['CDD'][list(jours_contrats).index(jour)] + 1

                            if types['CDD'][list(jours_contrats).index(jour)] > max:
                                max = types['CDD'][list(jours_contrats).index(jour)]

                        elif annonce[1] == 'FPT':
                            types['FPT'][list(jours_contrats).index(jour)] = types['FPT'][list(jours_contrats).index(jour)] + 1

                            if types['FPT'][list(jours_contrats).index(jour)] > max:
                                max = types['FPT'][list(jours_contrats).index(jour)]

                        elif annonce[1] == 'Stage':
                            types['Stage'][list(jours_contrats).index(jour)] = types['Stage'][list(jours_contrats).index(jour)] + 1

                            if types['Stage'][list(jours_contrats).index(jour)] > max:
                                max = types['Stage'][list(jours_contrats).index(jour)]

                        elif annonce[1] == 'Apprentissage':
                            types['Apprentissage'][list(jours_contrats).index(jour)] = types['Apprentissage'][list(jours_contrats).index(jour)] + 1

                            if types['Apprentissage'][list(jours_contrats).index(jour)] > max:
                                max = types['Apprentissage'][list(jours_contrats).index(jour)]

                        elif annonce[1] == 'VI':
                            types['VI'][list(jours_contrats).index(jour)] = types['VI'][list(jours_contrats).index(jour)] + 1

                            if types['VI'][list(jours_contrats).index(jour)] > max:
                                max = types['VI'][list(jours_contrats).index(jour)]

                        elif annonce[1] == 'Thèse':
                            types['Thèse'][list(jours_contrats).index(jour)] = types['Thèse'][list(jours_contrats).index(jour)] + 1

                            if types['Thèse'][list(jours_contrats).index(jour)] > max:
                                max = types['Thèse'][list(jours_contrats).index(jour)]

                        elif annonce[1] == 'Post doc':
                            types['Post doc'][list(jours_contrats).index(jour)] = types['Post doc'][list(jours_contrats).index(jour)] + 1

                            if types['Post doc'][list(jours_contrats).index(jour)] > max:
                                max = types['Post doc'][list(jours_contrats).index(jour)]

                        elif annonce[1] == 'Mission':
                            types['Mission'][list(jours_contrats).index(jour)] = types['Mission'][list(jours_contrats).index(jour)] + 1

                            if types['Mission'][list(jours_contrats).index(jour)] > max:
                                max = types['Mission'][list(jours_contrats).index(jour)]

                        elif annonce[1] == 'Autre':
                            types['Autre'][list(jours_contrats).index(jour)] = types['Autre'][list(jours_contrats).index(jour)] + 1

                            if types['Autre'][list(jours_contrats).index(jour)] > max:
                                max = types['Autre'][list(jours_contrats).index(jour)]

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
                        if annonce[1] == 'CDI':
                            types['CDI'][list(weeks).index(week)] = types['CDI'][list(weeks).index(week)] + 1

                            if types['CDI'][list(weeks).index(week)] > max:
                                max = types['CDI'][list(weeks).index(week)]

                        elif annonce[1] == 'CDD':
                            types['CDD'][list(weeks).index(week)] = types['CDD'][list(weeks).index(week)] + 1

                            if types['CDD'][list(weeks).index(week)] > max:
                                max = types['CDD'][list(weeks).index(week)]

                        elif annonce[1] == 'FPT':
                            types['FPT'][list(weeks).index(week)] = types['FPT'][list(weeks).index(week)] + 1

                            if types['FPT'][list(weeks).index(week)] > max:
                                max = types['FPT'][list(weeks).index(week)]

                        elif annonce[1] == 'Stage':
                            types['Stage'][list(weeks).index(week)] = types['Stage'][list(weeks).index(week)] + 1

                            if types['Stage'][list(weeks).index(week)] > max:
                                max = types['Stage'][list(weeks).index(week)]

                        elif annonce[1] == 'Apprentissage':
                            types['Apprentissage'][list(weeks).index(week)] = types['Apprentissage'][list(weeks).index(week)] + 1

                            if types['Apprentissage'][list(weeks).index(week)]\
                               > max:
                                max = types['Apprentissage'][list(weeks)
                                                             .index(week)]

                        elif annonce[1] == 'VI':
                            types['VI'][list(weeks).index(week)] = types['VI'][list(weeks).index(week)] + 1

                            if types['VI'][list(weeks).index(week)] > max:
                                max = types['VI'][list(weeks).index(week)]

                        elif annonce[1] == 'Thèse':
                            types['Thèse'][list(weeks).index(week)] = types['Thèse'][list(weeks).index(week)] + 1

                            if types['Thèse'][list(weeks).index(week)] > max:
                                max = types['Thèse'][list(weeks).index(week)]

                        elif annonce[1] == 'Post doc':
                            types['Post doc'][list(weeks).index(week)] = types['Post doc'][list(weeks).index(week)] + 1

                            if types['Post doc'][list(weeks).index(week)]\
                               > max:
                                max = types['Post doc'][list(weeks)
                                                        .index(week)]

                        elif annonce[1] == 'Mission':
                            types['Mission'][list(weeks).index(week)] = \
                            types['Mission'][list(weeks).index(week)] + 1

                            if types['Mission'][list(weeks).index(week)] > max:
                                max = types['Mission'][list(weeks).index(week)]

                        elif annonce[1] == 'Autre':
                            types['Autre'][list(weeks).index(week)] =\
                            types['Autre'][list(weeks).index(week)] + 1

                            if types['Autre'][list(weeks).index(week)] > max:
                                max = types['Autre'][list(weeks).index(week)]

                        data = {'max': max, 'types': types, 'legend': agreg}

                        with open('/home/pvernier/code/python/elpaso/static/json/contrats_' + periode + '.json', 'w') as f:
                            f.write(json.dumps(data))

if __name__ == '__main__':

    #print('Stand-alone execution')
    # DB connection settings
    db = path.abspath(r"../elpaso.sqlite")
    conn = sqlite3.connect(db)
    c = conn.cursor()
    # fetching the ID list
    c.execute("SELECT id FROM georezo")
    liste_input = [i[0] for i in c.fetchall()]
    #liste_input = c.fetchall()
    #print(liste_input)
    Fillin(liste_input).contrats(liste_input, c)

    # closing
    conn.close()
