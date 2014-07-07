# -*- coding: UTF-8 -*-
#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name:         Analyseur
# Purpose: 
#
# Author: @pvernier et @guts
#
# Python: 3.4.x
# Created: 18/04/2014
# Updated: 23/06/2014
# Licence: GPL 3
#-------------------------------------------------------------------------------

################################################################################
########### Libraries #############
###################################

# Standard library
from os import path
import re
import sqlite3
import threading # multi threads handling
from xml.etree import ElementTree as ET

# custom
from . import data
from . import LogGuy


################################################################################
############ Globals ##############
###################################

# logger object
logger = LogGuy.Logyk()

################################################################################
############ Classes ##############
###################################

class Analizer():
    """ analyse les dernière offres parues sur GeoRezo et enregistrées dans la table 
    georezo. """
    def __init__(self, liste_identifiants_offre, db_path=r"/home/pvernier/code/python/elpaso/elpaso.sqlite"):
        """ crée le curseur de connexion à la BD et répartit les tâches.
        liste_identifiants_offre = liste des ID des nouvelles offres """
        logger.append("Launching analyze")
        # connexion à la BD
        db = path.abspath(db_path)
        self.conn = sqlite3.connect(db)
        self.c  = self.conn.cursor()

        # extraction des types de contrats
        logger.append("\tParsing contrats")
        self.parse_contrats(liste_identifiants_offre, self.c)

        # extraction des lieux des offres
        logger.append("\tParsing lieux")
        self.parse_lieux(liste_identifiants_offre, self.c)

        # extraction des logiciels
        logger.append("\tParsing logiciels")
        self.parse_technos(liste_identifiants_offre, self.c)

        # extraction des métiers
        logger.append("\tParsing métiers")
        self.parse_metiers(liste_identifiants_offre, self.c)

        #### Disabling multithreading because of official documentation warning: https://docs.python.org/3/library/sqlite3.html#multithreading
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

        # fermeture de la connexion à la BD
        self.manage_connection(2)
        logger.append("Connection closed")

    def manage_connection(self, action):
        """ commit ou ferme la connexion à la demande """
        if action == 1:
            self.conn.commit()
        elif action == 2:
            self.conn.close()
        else:
            pass
        # end of function
        return self.conn


    def parse_contrats(self, li_id, db_cursor):
        """ extraction des types de contrats """
        for offre in li_id:
            db_cursor.execute("SELECT title FROM georezo WHERE id = " + str(offre))
            #c.execute("SELECT title FROM georezo WHERE id = ?", str(offre))
            titre = db_cursor.fetchone()
            contrat = titre[0].split(']')[0].lstrip('[')
            # insertion
            if contrat[0:3].lower() == 'cdi':
                db_cursor.execute("INSERT INTO contrats VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre), 1,0,0,0,0,0,0,0,0,""))
            elif contrat[0:3].lower() == 'cdd':
                db_cursor.execute("INSERT INTO contrats VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0, 1,0,0,0,0,0,0,0,""))
            elif "fpt" in contrat.lower():
                db_cursor.execute("INSERT INTO contrats VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0, 1,0,0,0,0,0,0,""))
            elif contrat.lower() == 'stage':
                db_cursor.execute("INSERT INTO contrats VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0,0, 1,0,0,0,0,0,""))
            elif "appr" in contrat.lower():
                db_cursor.execute("INSERT INTO contrats VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0,0,0, 1,0,0,0,0,""))
            elif "vi" in contrat.lower() or "volontariat" in contrat.lower():
                db_cursor.execute("INSERT INTO contrats VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0,0,0,0, 1,0,0,0,""))
            elif contrat.lower() == "thèse":
                db_cursor.execute("INSERT INTO contrats VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0,0,0,0,0, 1,0,0,""))
            elif "post" in contrat.lower():
                db_cursor.execute("INSERT INTO contrats VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0,0,0,0,0,0, 1,0,""))
            elif "mission" in contrat.lower() or "interim" in contrat.lower():
                db_cursor.execute("INSERT INTO contrats VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0,0,0,0,0,0,0, 1,""))
            else:
                db_cursor.execute("INSERT INTO contrats VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0,0,0,0,0,0,0,0, contrat))
            # Save (commit) the changes
            self.manage_connection(1)
            logger.append("{0} => Contrats parsed".format(str(offre)))
        # end of function
        # self.manage_connection(2)
        return li_id


    def parse_lieux(self, li_id, db_cursor):
        """ extraction des lieux des offres 
        liste des pays issues de : http://sql.sh/514-liste-pays-csv-xml"""
        for offre in li_id:
            db_cursor.execute("SELECT title FROM georezo WHERE id = " + str(offre))
            titre = db_cursor.fetchone()
            # trying to get the French departement code
            dpt_code = re.findall("(2[AB]|[0-9]+)", titre[0])
            if dpt_code:
                db_cursor.execute("INSERT INTO lieux VALUES (?,?,?)", (str(offre), str(dpt_code[0]), 3))
                self.manage_connection(1)
                logger.append("{0} ({1}) => Lieux parsed".format(str(offre), dpt_code))
                continue
            elif "idf" in titre[0].lower() or "Paris" in titre[0].lower() or "île de france" in titre[0].lower() or "île-de-france" in titre[0].lower():
                db_cursor.execute("INSERT INTO lieux VALUES (?,?,?)", (str(offre), str(75), 3))
                self.manage_connection(1)
                logger.append("{0} ({1}) => Lieux parsed".format(str(offre), "IDF"))
                continue
            elif any(pays.lower() in titre[0].lower() for pays in data.tup_pays):
                for pays in data.tup_pays:
                    if pays in titre[0]:
                        db_cursor.execute("INSERT INTO lieux VALUES (?,?,?)", (str(offre), pays, 1))
                        self.manage_connection(1)
                        logger.append("{0} ({1}) => Lieux parsed".format(str(offre), pays))
                        break
                    else:
                        continue
            elif any(ville.lower() in titre[0].lower() for ville in data.tup_villes_fr100):
                for ville in data.tup_villes_fr100:
                    if ville in titre[0]:
                        db_cursor.execute("INSERT INTO lieux VALUES (?,?,?)", (str(offre), ville, 4))
                        self.manage_connection(1)
                        logger.append("{0} ({1}) => Lieux parsed".format(str(offre), ville))
                        break
                    else:
                        continue
            else:
                pass
            # Save (commit) the changes
            self.manage_connection(1)
            logger.append("{0} ({1}) => Lieux parsed".format(str(offre), dpt_code))
        # end of function
        # self.manage_connection(2)
        return li_id


    def parse_technos(self, li_id, db_cursor):
        """ extraction des logiciels cités dans l'offre """
        for offre in li_id:
            li_values = [str(offre)]
            db_cursor.execute("SELECT content FROM georezo WHERE id = " + str(offre))
            contenu = db_cursor.fetchone()
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

            # adding the data into the database
            db_cursor.execute("INSERT INTO logiciels VALUES (?,?,?,?,?,?,?,?)", tuple(li_values))
            # Save (commit) the changes
            self.manage_connection(1)
            logger.append("{0} => Logiciels parsed. ".format(str(offre)))

        # end of function
        # self.manage_connection(2)
        return li_id

    def parse_metiers(self, li_id, db_cursor):
        """ extraction des métiers cités dans l'offre """
        for offre in li_id:
            li_values = [str(offre)]
            # getting the content
            db_cursor.execute("SELECT content FROM georezo WHERE id = " + str(offre))
            contenu = db_cursor.fetchone()
            contenu = self.remove_tags(contenu[0])

            # getting the title
            db_cursor.execute("SELECT title FROM georezo WHERE id = " + str(offre))
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

            # adding the data into the database
            db_cursor.execute("INSERT INTO metiers VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", tuple(li_values))
            # Save (commit) the changes
            self.manage_connection(1)
            logger.append("{0} => Métiers parsed".format(str(offre)))
        # end of function
        # self.manage_connection(2)
        return li_id

    def remove_tags(self, html_text):
        """ nettoie les balises HTML du contenu des offres """
        try:
            text = ''.join(ET.fromstring(html_text).itertext())
        except:
            TAG_RE = re.compile(r'<[^>]+>')
            return TAG_RE.sub('', html_text)
        # end of function
        return text.lower()

################################################################################
###### Stand alone program ########
###################################

if __name__ == '__main__':
    u""" standalone execution for tests. Paths are relative considering a test
    within the official repository (https://github.com/Guts/DicoShapes/)"""
    # libraries import
    # from os import path, getcwd
    # import sqlite3
    #
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

