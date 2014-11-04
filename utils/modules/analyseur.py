# -*- coding: UTF-8 -*-
#!/usr/bin/env python

#------------------------------------------------------------------------------
# Name:         Analyseur (or Analizer in English)
# Purpose:      Analyzes the offers published on GeoRezo, extracts and formats
#               interesting informations: contracts types, date, etc.
#
# Authors:      pvernier (https://github.com/pvernier)
#               & Guts (https://github.com/Guts)
#
# Python:       3.4.x
# Created:      01/05/2014
# Updated:      03/11/2014
#
# Licence:      GPL 3
#------------------------------------------------------------------------------

###############################################################################
########### Libraries #############
###################################

# Standard library
from os import path
import re
import sqlite3
# import threading # multi threads handling
from xml.etree import ElementTree as ET

# third party libraries
import nltk
from nltk.corpus import stopwords

# custom
from . import data
from . import LogGuy

###############################################################################
############ Globals ##############
###################################

# logger object
logger = LogGuy.Logyk()

###############################################################################
############ Classes ##############
###################################


class Analizer():
    """
    analyze of last offers published on GeoRezo and stored in the main table.
    """
    def __init__(self, liste_identifiants_offre, db_path=r"../../elpaso.sqlite"):
        """
        manage the connection cursor and task related

        liste_identifiants_offre = IDs list of offers to process
        """
        # a little log message to know where we are
        logger.append("Launching analyze")

        # connection to the DB
        db = path.abspath(db_path)
        self.conn = sqlite3.connect(db)
        self.c = self.conn.cursor()

        # extraction of types of contracts
        logger.append("\tParsing contrats")
        self.parse_contrats(liste_identifiants_offre, self.c)

        # extraction of places
        logger.append("\tParsing lieux")
        self.parse_lieux(liste_identifiants_offre, self.c)

        # extraction of software
        logger.append("\tParsing logiciels")
        self.parse_technos(liste_identifiants_offre, self.c)

        # extraction of types of job
        logger.append("\tParsing métiers")
        self.parse_metiers(liste_identifiants_offre, self.c)

        # extraction of words semantic
        logger.append("\tParsing termes")
        self.parse_words(liste_identifiants_offre, self.c)

        ###############
        ## Disabling multithreading because of official documentation warning
        ## see: https://docs.python.org/3/library/sqlite3.html#multithreading
        # tr_contrats = threading.Thread(target=self.parse_contrats,
        #                                args=(liste_identifiants_offre, self.c))
        # tr_contrats.daemon = True
        # tr_contrats.run()

        # # extraction des lieux des offres
        # tr_lieux = threading.Thread(target=self.parse_lieux,
        #                             args=(liste_identifiants_offre, self.c))
        # tr_lieux.daemon = True
        # tr_lieux.run()

        # # extraction des logiciels
        # tr_techno = threading.Thread(target=self.parse_technos,
        #                                args=(liste_identifiants_offre, self.c))
        # tr_techno.daemon = True
        # tr_techno.run()
        #################

        # closing connection
        self.manage_connection(2)
        logger.append("Connection closed")

    def manage_connection(self, action):
        """
        perform actions depending on the parameter:
        1 = commit/save
        2 = close
        """
        if action == 1:
            self.conn.commit()
        elif action == 2:
            self.conn.close()
        else:
            pass
        # end of function
        return self.conn

    def parse_contrats(self, li_id, db_cursor):
        """
        Extraction of types of contracts: CDI, CDD, mission, volontariat, etc.
        In theory, the offer's title is formatted to contain the type between []

        li_id = list of offers'IDs to process
        db_cursor = connection cursor to the DB where to store extracted data
        """
        # looping on the offers list
        for offre in li_id:
            # get the offer from the main table
            db_cursor.execute("SELECT title FROM georezo WHERE id = {0}".format(str(offre)))
            # get the title
            titre = db_cursor.fetchone()
            # clean the title: excluding text out of brackets
            contrat = titre[0].split(']')[0].lstrip('[')
            # depending on the type found, inserting into the DB
            if contrat[0:3].lower() == 'cdi':
                db_cursor.execute("INSERT INTO contrats VALUES \
                    (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),1,0,0,0,0,0,0,0,0,""))
            elif contrat[0:3].lower() == 'cdd':
                db_cursor.execute("INSERT INTO contrats VALUES \
                    (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,1,0,0,0,0,0,0,0,""))
            elif "fpt" in contrat.lower()\
                or "fpe" in contrat.lower()\
                or "ftp" in contrat.lower():
                db_cursor.execute("INSERT INTO contrats VALUES \
                    (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0,1,0,0,0,0,0,0,""))
            elif "stage" in contrat.lower():
                db_cursor.execute("INSERT INTO contrats VALUES \
                    (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0,0,1,0,0,0,0,0,""))
            elif "appr" in contrat.lower():
                db_cursor.execute("INSERT INTO contrats VALUES \
                    (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0,0,0,1,0,0,0,0,""))
            elif "vi" in contrat.lower() \
                or "volontariat" in contrat.lower()\
                or "vsc" in contrat.lower():
                db_cursor.execute("INSERT INTO contrats VALUES \
                    (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0,0,0,0,1,0,0,0,""))
            elif "these" in contrat.lower() or "thèse" in contrat.lower():
                db_cursor.execute("INSERT INTO contrats VALUES \
                    (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0,0,0,0,0,1,0,0,""))
            elif "post" in contrat.lower():
                db_cursor.execute("INSERT INTO contrats VALUES \
                    (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0,0,0,0,0,0,1,0,""))
            elif "mission" in contrat.lower() \
                or "interim" in contrat.lower()\
                or "intérim" in contrat.lower():
                db_cursor.execute("INSERT INTO contrats VALUES \
                    (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0,0,0,0,0,0,0,1,""))
            else:
                db_cursor.execute("INSERT INTO contrats VALUES \
                    (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0,0,0,0,0,0,0,0,contrat))
            # Save (commit) the changes
            self.manage_connection(1)
            logger.append("{0} => Contrats parsed".format(str(offre)))
        # end of function
        return li_id

    def parse_lieux(self, li_id, db_cursor):
        """
        Extraction of places of contracts: regions, countries, cities, etc.
        In theory, offer's title is formatted to contain the place between ()

        li_id = list of offers'IDs to process
        db_cursor = connection cursor to the DB where to store extracted data
        
        Countries list from: http://sql.sh/514-liste-pays-csv-xml
        """
        # looping on the offers list
        for offre in li_id:
            # get the offer from the main table
            db_cursor.execute("SELECT title FROM georezo WHERE id = {0}".format(str(offre)))
            # get the title
            titre = db_cursor.fetchone()
            # clean the title: get the text after the closing bracket
            try:
                titre = titre[0][titre[0].index("]") + 1:len(titre[0])]
            except ValueError:
                # if title is not correctly formatted, just get it the raw
                logger.append("\n\t==== ERRREUR : formatage titre de l'offre.")
                titre = titre[0]
            # trying to get the French departement code with a regex
            dpt_code = re.findall("(2[AB]|[0-9]+)", titre)
            # depending on the result, classify the place according to the
            # territory scale
            if dpt_code:
                db_cursor.execute("INSERT INTO lieux VALUES (?,?,?,?)",\
                    (str(offre), str(dpt_code[0]), 3, ""))
                # saving the  change because there are offers which contain
                # other type of place information. ie: 33 (France)
                self.manage_connection(1)
                # a little log
                logger.append("{0} ({1}) => Lieux parsed".format(str(offre),
                                                                 dpt_code))
                continue
            elif "idf" in titre.lower() \
                or "Paris" in titre.lower() \
                or "île de france" in titre.lower() \
                or "île-de-france" in titre[0].lower():
                db_cursor.execute("INSERT INTO lieux VALUES (?,?,?,?)",\
                    (str(offre), str(75), 3, ""))
                # saving the  change because there are offers which contain
                # other type of place information. ie: 33 (France)
                self.manage_connection(1)
                # a little log
                logger.append("{0} ({1}) => Lieux parsed".format(str(offre), "IDF"))
                continue
            elif any(pays.lower() in titre.lower() for pays in data.tup_pays):
                for pays in data.tup_pays:
                    if pays in titre:
                        db_cursor.execute("INSERT INTO lieux VALUES (?,?,?,?)",\
                            (str(offre), pays, 1, ""))
                        # saving the  change because there are offers which
                        # contain other type of place information. ie: 33 (France)
                        self.manage_connection(1)
                        # a little log
                        logger.append("{0} ({1}) => Lieux parsed".format(str(offre),
                                                                         pays))
                        break
                    else:
                        continue
            elif any(ville.lower() in titre.lower() for ville in data.tup_villes_fr100):
                for ville in data.tup_villes_fr100:
                    if ville in titre:
                        db_cursor.execute("INSERT INTO lieux VALUES (?,?,?,?)",
                            (str(offre), ville, 4, ""))
                        # saving the  change because there are offers which
                        # contain other type of place information. ie: 33 (France)
                        self.manage_connection(1)
                        # a little log
                        logger.append("{0} ({1}) => Lieux parsed".format(str(offre),
                                                                         ville))
                        break
                    else:
                        continue
            else:
                pass
            # Save (commit) the changes
            self.manage_connection(1)
            logger.append("{0} ({1}) => Lieux parsed".format(str(offre), dpt_code))
        # end of function
        return li_id

    def parse_technos(self, li_id, db_cursor):
        """
        Extraction of softwares mentioned into the offers: ArcGIS, QGIS, etc.
        Softwares are usually mentioned in the offer body and it could be hard
        to distinct the names. It's based on a list stored in data.py

        li_id = list of offers'IDs to process
        db_cursor = connection cursor to the DB where to store extracted data
        """
        # looping on the offers list
        for offre in li_id:
            # local list of values to insert at the end of loop
            li_values = [str(offre)]
            # 
            db_cursor.execute("SELECT content FROM georezo WHERE {0}".format(str(offre)))
            contenu = db_cursor.fetchone()
            # clean the content removing HTML tags
            contenu = self.remove_tags(contenu[0])
            # testing softwares recognition
            if any(software in contenu.lower() for software in data.tup_prop):
                """ filtre les logiciels propriétaires """
                li_values.append(1)
            else:
                li_values.append(0)
            if any(software in contenu.lower() for software in data.tup_opso):
                """ filtre les logiciels libres """
                li_values.append(1)
            else:
                li_values.append(0)
            if any(software in contenu.lower() for software in data.tup_sgbd):
                """ filtre les systèmes de gestion de bases de données """
                li_values.append(1)
            else:
                li_values.append(0)
            if any(software in contenu.lower() for software in data.tup_prog):
                """ filtre les langages de programmation """
                li_values.append(1)
            else:
                li_values.append(0)
            if any(software in contenu.lower() for software in data.tup_web):
                """ filtre le développement web """
                li_values.append(1)
            else:
                li_values.append(0)
            if any(software in contenu.lower() for software in data.tup_cdao):
                """ filtre les logiciels de dessin assisté """
                li_values.append(1)
            else:
                li_values.append(0)
            if any(software in contenu.lower() for software in data.tup_teldec):
                """ filtre les logiciels de télédétection """
                li_values.append(1)
            else:
                li_values.append(0)

            li_values.append("")
            # adding the data into the database
            db_cursor.execute("INSERT INTO logiciels VALUES (?,?,?,?,?,?,?,?,?)", tuple(li_values))
            # Save (commit) the changes
            self.manage_connection(1)
            logger.append("{0} => Logiciels parsed. ".format(str(offre)))

        # end of function
        return li_id

    def parse_metiers(self, li_id, db_cursor):
        """
        Extraction of types of jobs mentioned into the offers: cartographer,
        GIS analyst, engineer, etc.
        Jobs'labels are usually mentioned into the offer body and it can be hard
        to distinct the names. It's based on a list written in data.py

        li_id = list of offers'IDs to process
        db_cursor = connection cursor to the DB where to store extracted data
        """
        for offre in li_id:
            li_values = [str(offre)]
            # get the content
            db_cursor.execute("SELECT content FROM georezo WHERE id = {0}".format(str(offre)))
            contenu = db_cursor.fetchone()
            contenu = self.remove_tags(contenu[0])

            # get the title
            db_cursor.execute("SELECT title FROM georezo WHERE id = {0}".format(str(offre)))
            titre = db_cursor.fetchone()

            if any(metier in titre[0].lower() for metier in ("administrateur", "administration")):
                li_values.append(2)
            elif any(metier in contenu.lower() for metier in ("administrateur", "administration")):
                li_values.append(1)
            else:
                li_values.append(0)

            if any(metier in titre[0].lower() for metier in ("cartographe", "cartographie")):
                li_values.append(2)
            elif any(metier in contenu.lower() for metier in ("cartographe", "cartographie")):
                li_values.append(1)
            else:
                li_values.append(0)

            if any(metier in titre[0].lower() for metier in ("chargé d'étude", "chargé d'études")):
                li_values.append(2)
            elif any(metier in contenu.lower() for metier in ("chargé d'étude", "chargé d'études")):
                li_values.append(1)
            else:
                li_values.append(0)

            if any(metier in titre[0].lower() for metier in ("chargé de mission", "chargé de missions")):
                li_values.append(2)
            elif any(metier in contenu.lower() for metier in ("chargé de mission", "chargé de missions")):
                li_values.append(1)
            else:
                li_values.append(0)

            if any(metier in titre[0].lower() for metier in ("chef de projet",)):
                li_values.append(2)
            elif any(metier in contenu.lower() for metier in ("chef de projet",)):
                li_values.append(1)
            else:
                li_values.append(0)

            if any(metier in titre[0].lower() for metier in ("géomètre expert", "géomètre", "dessinateur")):
                li_values.append(2)
            elif any(metier in contenu.lower() for metier in ("géomètre expert", "géomètre", "dessinateur")):
                li_values.append(1)
            else:
                li_values.append(0)

            if any(metier in titre[0].lower() for metier in ("ingénieur", "ingénieur d'étude")):
                li_values.append(2)
            elif any(metier in contenu.lower() for metier in ("ingénieur", "ingénieur d'étude")):
                li_values.append(1)
            else:
                li_values.append(0)

            if any(metier in titre[0].lower() for metier in ("responsable", "en charge de", "en charge du")):
                li_values.append(2)
            elif any(metier in contenu.lower() for metier in ("responsable", "en charge de", "en charge du")):
                li_values.append(1)
            else:
                li_values.append(0)

            if any(metier in titre[0].lower() for metier in ("sigiste", "SIG")):
                li_values.append(2)
            elif any(metier in contenu.lower() for metier in ("sigiste", "SIG")):
                li_values.append(1)
            else:
                li_values.append(0)

            if any(metier in titre[0].lower() for metier in ("technicien",)):
                li_values.append(2)
            elif any(metier in contenu.lower() for metier in ("technicien",)):
                li_values.append(1)
            else:
                li_values.append(0)

            if any(metier in titre[0].lower() for metier in ("topograph",)):
                li_values.append(2)
            elif any(metier in contenu.lower() for metier in ("topograph",)):
                li_values.append(1)
            else:
                li_values.append(0)

            if any(metier in titre[0].lower() for metier in ("géomatique", "géomaticien", "développeur")):
                li_values.append(2)
            elif any(metier in contenu.lower() for metier in ("géomatique", "géomaticien", "développeur")):
                li_values.append(1)
            else:
                li_values.append(0)

            li_values.append("")

            # adding the data into the database
            db_cursor.execute("INSERT INTO metiers VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", tuple(li_values))
            # Save (commit) the changes
            self.manage_connection(1)
            logger.append("{0} => Métiers parsed".format(str(offre)))
        # end of function
        return li_id

    def parse_words(self, li_id, db_cursor):
        """
        Extraction of words mentioned into the offers. The goal is to perform
        a semantic analysis.
        It's based on NLTK: http://www.nltk.org

        li_id = list of offers'IDs to process
        db_cursor = connection cursor to the DB where to store extracted data
        """
        # get list of common French words to filter
        stop_fr = set(stopwords.words('french'))   # add specific French

        # custom list
        li_stop_custom = ['(', ')', '.',':',';','/','nbsp','&','#',',','-',':',\
                          'http', 'img', 'br', 'amp', '<', '>', '%', 'border', 'border=']

        # looping on the offers list
        for offre in li_id:
            # list to store words OK
            li_words_ok = []
            # dictionary of words/frequency
            dict_words_frek = {}
            # get the content
            db_cursor.execute("SELECT content FROM georezo WHERE id = {0}".format(str(offre)))
            contenu = db_cursor.fetchone()
            # basic clean of the content
            contenu = self.remove_tags(contenu[0])
            # tokenizing and cleaning html tags
            # contenu = nltk.word_tokenize(nltk.clean_html(contenu))
            contenu = nltk.word_tokenize(contenu)
            # filtering
            for mot in contenu:
                if mot not in stop_fr and mot not in li_stop_custom and len(mot) > 2:
                    li_words_ok.append(mot)
                else:
                    pass

            # calc words frequency
            for mot in li_words_ok:
                if mot in dict_words_frek:
                    dict_words_frek[mot] = dict_words_frek.get(mot) + 1
                else:
                    dict_words_frek[mot] = 1

            # storing words frequency
            for mot in sorted(dict_words_frek.keys()):
                # test s'il est déjà présent dans la BD
                arecup = (mot, )
                db_cursor.execute('SELECT * FROM semantique WHERE word=?', arecup)
                row = db_cursor.fetchone()
                if row:
                    # S'il est déjà présent on met à jour les occurences
                    db_cursor.execute("UPDATE semantique SET frequency = ? WHERE word= ?", (row[1] + dict_words_frek.get(mot), mot))
                    print('mot existant : {0} x {1}'.format(mot, dict_words_frek.get(mot)))
                else:
                    # Sinon, on l'ajoute à la BD
                    db_cursor.execute("INSERT INTO semantique VALUES (?, ?)", (mot, dict_words_frek.get(mot)))
                    print('nouveau mot : {0}'.format(mot))

            # commit changes
            self.manage_connection(1)

        # end of function
        return

    def remove_tags(self, html_text):
        """
        very basic cleaner for HTML markups
        """
        try:
            text = ''.join(ET.fromstring(html_text).itertext())
        except:
            TAG_RE = re.compile(r'<[^>]+>')
            return TAG_RE.sub('', html_text)
        # end of function
        return text.lower()

###############################################################################
###### Stand alone program ########
###################################

if __name__ == '__main__':
    u"""
    standalone execution.
    """
    print('Stand-alone execution')
    # DB connection settings
    db = path.abspath(r"../elpaso.sqlite")
    conn = sqlite3.connect(db)
    c = conn.cursor()
    # fetching the ID list
    c.execute("SELECT id FROM georezo")
    liste_input = [i[0] for i in c.fetchall()]
    #liste_input = c.fetchall()
    print(liste_input)
    Analizer(liste_input, db).parse_technos(liste_input)

    # closing
    conn.close()
