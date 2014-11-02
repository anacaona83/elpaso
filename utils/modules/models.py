from os import path, environ, listdir
import sys
import sqlite3
import json
import time
from datetime import date as dt, datetime
from . import LogGuy

sys.path.append('/home/pvernier/code/python/elpaso')
environ['DJANGO_SETTINGS_MODULE'] = 'elpaso.settings'
from jobs.models import Contrat
from jobs.models import Year
from jobs.models import Month
from jobs.models import Week

# logger object
logger = LogGuy.Logyk()


class Fillin():
    def __init__(self, liste_identifiants_offre):
        '''liste_identifiants_offre = liste des ID des nouvelles offres'''
        # connexion à la BD EL Paso
        db = path.abspath('/home/pvernier/code/python/elpaso/elpaso.sqlite')
        self.conn = sqlite3.connect(db)
        self.c = self.conn.cursor()

        # connexion à la BD Django - NO MORE NEEDED
        # db_django = path.abspath('/home/pvernier/code/python/elpaso/elpaso.sqlite')
        # self.conn_django = sqlite3.connect(db_django)
        # self.c_django = self.conn_django.cursor()

        # Remplissage des contrats dans la BD django
        logger.append("\tFill in contrats in the Django DB")
        self.contrats(liste_identifiants_offre, self.c)

        logger.append("\tCreate JSON files")
        self.create_json('year')
        self.create_json('month')
        self.create_json('week')
        self.create_json('day')

        self.periodizer(liste_identifiants_offre, self.c)

    def check_date(self, annee, mois, semaine):
        '''
        Vérifie que la date du jour existe dans les 3 tables de périodes
        (année, mois, semaines) et créent les lignes correspondantes
        le cas échéant.
        '''
        # # Date du jour, numéro et 1er jour de la semaine actuelle
        # today = dt.today()
        # week_nb = dt(today.year, today.month, today.day).isocalendar()[1]

        first_day = time.asctime(time.strptime('{0} {1} 1'.format(annee,
                                     semaine - 1), '%Y %W %w'))
        first_day = datetime.strptime(first_day, "%a %b %d %H:%M:%S %Y")

        # récupération des périodes dans la BDD
        result_month = Month.objects.filter(month=mois,
                                            year= annee)
        result_year = Year.objects.filter(year= annee)
        result_week = Week.objects.filter(week=semaine,
                                          year=annee)

        # check des résultats des requêtes et création le cas échéant
        if len(result_month) == 0:
            # calcul du timestamp en millisecond
            month_timestamp = time.mktime(dt(annee, mois, 1).timetuple()) * 1000
            # mise à jour de la table en créant la ligne correspondante
            update_month = Month(month=mois, year=annee, month_milsec=month_timestamp)
            # sauvegarde / commit
            update_month.save()
        else:
            pass

        if len(result_year) == 0:
            year_timestamp = time.mktime(dt(annee, 1, 1).timetuple()) * 1000
            update_year = Year(year=annee, year_milsec=year_timestamp)
            update_year.save()
        else:
            pass

        if len(result_week) == 0:
            week_timestamp = time.mktime(first_day.timetuple()) * 1000
            update_week = Week(year=annee, week_milsec=week_timestamp, week=semaine)
            update_week.save()
        else:
            pass

    def periodizer(self, li_id, db_cursor):
        ''' TO DO '''
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
            try:
              date_object = datetime.strptime(date[0],
                                            "%a, %d %b %Y %H:%M:%S +0200")
            except ValueError:
              date_object = datetime.strptime(date[0],
                                            "%a, %d %b %Y %H:%M:%S +0100")

            # découpage de la date
            year = date_object.year
            month_number = date_object.month
            day_number = date_object.day
            week = dt(year, month_number, day_number).isocalendar()[1]
            first_day = time.asctime(time.strptime('{0} {1} 1'.format(year,
                                     week - 1), '%Y %W %w'))
            first_day = datetime.strptime(first_day, "%a %b %d %H:%M:%S %Y")

            # check if date exists in DB
            self.check_date(year, month_number, week)

            # récupération des offres par périodes  : années, mois, semaines
            db_cursor.execute('SELECT * FROM jobs_year WHERE year = ' +
                              str(year))
            val_year = db_cursor.fetchall()

            db_cursor.execute('SELECT * FROM jobs_month WHERE year = ' +
                              str(year) + ' AND month = ' + str(month_number))
            val_month = db_cursor.fetchall()


            db_cursor.execute('SELECT * FROM jobs_week WHERE year = ' +
                              str(year) + ' AND week = ' + str(week))
            val_week = db_cursor.fetchall()

            if len(contrat) > 0:
                if contrat[0][1] == 1:
                    db_cursor.execute('UPDATE jobs_year SET cdi = ' +
                                      str(val_year[0][2] + 1) + ' WHERE year \
                                      = ' + str(year))
                    db_cursor.execute('UPDATE jobs_month SET cdi = ' +
                                      str(val_month[0][3] + 1) + ' WHERE year \
                                      = {0} AND month = {1}'.format(str(year),
                                      str(month_number)))
                    db_cursor.execute('UPDATE jobs_week SET cdi = ' +
                                      str(val_week[0][4] + 1) + ' WHERE year \
                                      = {0} AND week = {1}'.format(str(year),
                                      str(week)))

                elif contrat[0][2] == 1:
                    db_cursor.execute('UPDATE jobs_year SET cdd = ' +
                                      str(val_year[0][3] + 1) + ' WHERE year \
                                       = ' + str(year))
                    db_cursor.execute('UPDATE jobs_month SET cdd = ' +
                                      str(val_month[0][4] + 1) + ' WHERE year \
                                      = {0} AND month = {1}'.format(str(year),
                                      str(month_number)))
                    db_cursor.execute('UPDATE jobs_week SET cdd = ' +
                                      str(val_week[0][5] + 1) + ' WHERE year \
                                      = {0} AND week = {1}'.format(str(year),
                                      str(week)))

                elif contrat[0][3] == 1:
                    db_cursor.execute('UPDATE jobs_year SET fpt = ' +
                                      str(val_year[0][4] + 1) + ' WHERE year \
                                      = ' + str(year))
                    db_cursor.execute('UPDATE jobs_month SET fpt = ' +
                                      str(val_month[0][5] + 1) + ' WHERE year \
                                      = {0} AND month = {1}'.format(str(year),
                                      str(month_number)))
                    db_cursor.execute('UPDATE jobs_week SET fpt = ' +
                                      str(val_week[0][6] + 1) + ' WHERE year \
                                      = {0} AND week = {1}'.format(str(year),
                                      str(week)))

                elif contrat[0][4] == 1:
                    db_cursor.execute('UPDATE jobs_year SET stage = ' +
                                      str(val_year[0][5] + 1) + ' WHERE year \
                                      = ' + str(year))
                    db_cursor.execute('UPDATE jobs_month SET stage = ' +
                                      str(val_month[0][6] + 1) + ' WHERE year \
                                      = {0} AND month = {1}'.format(str(year),
                                      str(month_number)))
                    db_cursor.execute('UPDATE jobs_week SET stage = ' +
                                      str(val_week[0][7] + 1) + ' WHERE year \
                                      = {0} AND week = {1}'.format(str(year),
                                      str(week)))

                elif contrat[0][5] == 1:
                    db_cursor.execute('UPDATE jobs_year SET apprentissage = ' +
                                      str(val_year[0][6] + 1) + ' WHERE year \
                                      = ' + str(year))
                    db_cursor.execute('UPDATE jobs_month SET apprentissage = \
                                      ' + str(val_month[0][7] + 1) + ' WHERE \
                                      year  = {0} AND month = {1}'.format(str(
                                      year), str(month_number)))
                    db_cursor.execute('UPDATE jobs_week SET apprentissage = ' +
                                      str(val_week[0][8] + 1) + ' WHERE year \
                                      = {0} AND week = {1}'.format(str(year),
                                      str(week)))

                elif contrat[0][6] == 1:
                    db_cursor.execute('UPDATE jobs_year SET vi = ' +
                                      str(val_year[0][7] + 1) + ' WHERE year \
                                      = ' + str(year))
                    db_cursor.execute('UPDATE jobs_month SET vi = ' +
                                      str(val_month[0][8] + 1) + ' WHERE year \
                                      = {0} AND month = {1}'.format(str(year),
                                      str(month_number)))
                    db_cursor.execute('UPDATE jobs_week SET vi = ' +
                                      str(val_week[0][9] + 1) + ' WHERE year \
                                      = {0} AND week = {1}'.format(str(year),
                                      str(week)))

                elif contrat[0][7] == 1:
                    db_cursor.execute('UPDATE jobs_year SET these = ' +
                                      str(val_year[0][8] + 1) + ' WHERE year \
                                      = ' + str(year))
                    db_cursor.execute('UPDATE jobs_month SET these = ' +
                                      str(val_month[0][9] + 1) + ' WHERE year \
                                      = {0} AND month = {1}'.format(str(year),
                                      str(month_number)))
                    db_cursor.execute('UPDATE jobs_week SET these = ' +
                                      str(val_week[0][10] + 1) + ' WHERE year \
                                      = {0} AND week = {1}'.format(str(year),
                                      str(week)))

                elif contrat[0][8] == 1:
                    db_cursor.execute('UPDATE jobs_year SET post_doc = ' +
                                      str(val_year[0][9] + 1) + ' WHERE year \
                                      = ' + str(year))
                    db_cursor.execute('UPDATE jobs_month SET post_doc = ' +
                                      str(val_month[0][10] + 1) + ' WHERE year\
                                      = {0} AND month = {1}'.format(str(year),
                                      str(month_number)))
                    db_cursor.execute('UPDATE jobs_week SET post_doc = ' +
                                      str(val_week[0][11] + 1) + ' WHERE year \
                                      = {0} AND week = {1}'.format(str(year),
                                      str(week)))

                elif contrat[0][9] == 1:
                    db_cursor.execute('UPDATE jobs_year SET mission = ' +
                                      str(val_year[0][10] + 1) + ' WHERE year\
                                      = ' + str(year))
                    db_cursor.execute('UPDATE jobs_month SET mission = ' +
                                      str(val_month[0][11] + 1) + ' WHERE year\
                                      = {0} AND month = {1}'.format(str(year),
                                      str(month_number)))
                    db_cursor.execute('UPDATE jobs_week SET mission = ' +
                                      str(val_week[0][12] + 1) + ' WHERE year\
                                      = {0} AND week = {1}'.format(str(year),
                                      str(week)))

                elif contrat[0][10]:
                    db_cursor.execute('UPDATE jobs_year SET autre = ' +
                                      str(val_year[0][11] + 1) + ' WHERE year\
                                      = ' + str(year))
                    db_cursor.execute('UPDATE jobs_month SET autre = ' +
                                      str(val_month[0][12] + 1) + ' WHERE year\
                                      = {0} AND month = {1}'.format(str(year),
                                      str(month_number)))
                    db_cursor.execute('UPDATE jobs_week SET autre = ' +
                                      str(val_week[0][13] + 1) + ' WHERE year\
                                      = {0} AND week = {1}'.format(str(year),
                                      str(week)))

                self.conn.commit()

                # Pour remplir la colonne first_day
                if val_week[0][3] is None:
                    db_cursor.execute('UPDATE jobs_week SET first_day = "{0}" WHERE year = {1} AND week = {2}'.format(str(first_day), str(year), str(week)))
                    self.conn.commit()
                else:
                    pass

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
            try:
              date_object = datetime.strptime(date[0], "%a, %d %b %Y \
                                            %H:%M:%S +0200")
            except ValueError:
              date_object = datetime.strptime(date[0], "%a, %d %b %Y \
                                            %H:%M:%S +0100")


            # Je récupère les infos sur les lieux
            db_cursor.execute("SELECT lieu_lib, lieu_type FROM lieux WHERE id = " + str(offre))
            # Je récupère ces infos dans la variable 'lieux'
            lieux = db_cursor.fetchall()

            if len(contrat) > 0:
                if contrat[0][1] == 1:
                    type_contrat = 'cdi'

                elif contrat[0][2] == 1:
                    type_contrat = 'cdd'

                elif contrat[0][3] == 1:
                    type_contrat = 'fpt'

                elif contrat[0][4] == 1:
                    type_contrat = 'stage'

                elif contrat[0][5] == 1:
                    print(str(offre))
                    type_contrat = 'apprentissage'

                elif contrat[0][6] == 1:
                    type_contrat = 'vi'

                elif contrat[0][7] == 1:
                    type_contrat = 'these'

                elif contrat[0][8] == 1:
                    type_contrat = 'post doc'

                elif contrat[0][9] == 1:
                    type_contrat = 'mission'

                elif contrat[0][10]:
                    type_contrat = 'autre'

                # Je traite les lieux
                # Ces conditions seront à changer plus tard
                # Il ne devrait pas y avoir autant de cas

                # Le code commenté ci-dessous n'est pas bon

                # Departement
                # if lieux[0][1] == '3':
                #     if (len(lieux[0][0]) == 2 or len(lieux[0][0]) == 3):
                #         dept = lieux[0][0]
                #     elif len(lieux[0][0]) == 1:
                #         dept = '0' + lieux[0][0]
                #     elif len(lieux[0][0]) > 3:
                #         dept = lieux[0][0][0:2]
                #     # Ne devrait pas être nécessaire
                #     else:
                #         dept = '99'
                #     pays = 'France'
                # # Pays
                # else:
                #     pays = lieux[0][1]
                #     dept = '99'

                db_cursor.execute('INSERT INTO jobs_contrat VALUES \
                                      (?,?,?,?,?,?,?)', (str(offre),
                                      type_contrat, date_object,
                                      date_object.isocalendar()[1],
                                      date_object.isocalendar()[2],
                                      '', ''))

                self.conn.commit()

    def create_json2(self, periode):
        """  """
        # récupérer la liste des types de contrats
        types_contrat = Contrat.objects.values('type')
        types = [{'key': t, 'values': []} for t in types_contrats]

        # timestamps en milliseconds
        ts_year = Year.objects.values('year_milsec')
        ts_month = Month.objects.values('month_milsec')
        ts_week = Week.objects.values('week_milsec')

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

        # # parcourir la table de chaque période (cad 3 fois). Faire gaffe aux futures lignes vides (déjà créées)
        # for month, cdi in ts_month:
        #     print(month, month_cdi[ts_month.index(month)]




        # récupérer une ligne, calculer le timestamp de chaque ligne, récupérer la valeur de chaque type et le rentrer dans le dictionnaire



        # sérialiser le dico en json

        data = {'cdi': [[1398895200, 12], [1401573600, 14 ]],
                 'cdd': [[1398895200, 10], [1401573600, 9 ]],
                 'stage': [[1398895200, 5], [1401573600, 7 ]]
                }

        with open('/home/pvernier/code/python/elpaso/static/json/contrats2_' + periode + '.json', 'w') as f:
                            f.write(json.dumps(data))


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

        # Je traite les lieux
        # Je fais un CSV par mois et par année qui contiennent tous les
        # types de contrats pour ce mois ou cette année

        # Je dois savoir si le ficheir CSV correspondant à la date existe
        # déjà (dans ce cas je dois l'éditer) ou s'il faut que j'en créé
        # un nouveau

        # structure des noms de fichiers CSV :
        # 2014_01.csv (mois)
        # 2014_12.csv
        # 2014.csv (année)
        # 2015.csv

        # Je dois donc récupérer le mois et l'année de l'offre et comparer
        # avec le dernier fichier CSV (des mois et des années)

        # Les années
        files_year = listdir('/home/pvernier/code/python/elpaso/static/csv/year')

        # Les mois
        files_month = listdir('/home/pvernier/code/python/elpaso/static/csv/month')


if __name__ == '__main__':

    #print('Stand-alone execution')
    # DB connection settings
    db = path.abspath(r"../elpaso.sqlite")
    conn = sqlite3.connect(db)
    c = conn.cursor()
    # fetching the ID list
    c.execute("SELECT id FROM georezo")
    liste_input = [i[0] for i in c.fetchall()]
    #print(liste_input)
    Fillin(liste_input).contrats(liste_input, c)

    # closing
    conn.close()
