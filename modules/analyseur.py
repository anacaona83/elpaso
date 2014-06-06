# -*- coding: UTF-8 -*-
#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name: Analyseur
# Purpose: 
#
# Author: @pvernier et @guts
#
# Python: 3.4.x
# Created: 18/04/2014
# Updated: 15/05/2014
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


################################################################################
########### Classes #############
###################################

class Analizer():
    """ analyse les dernière offres parues sur GeoRezo et enregistrées dans la table 
    georezo. """
    def __init__(self, liste_identifiants_offre, db_path=r"elpaso.sqlite"):
        """ crée le curseur de connexion à la BD et répartit les tâches.
        liste_identifiants_offre = liste des ID des nouvelles offres """
        # connexion à la BD
        db = path.abspath(db_path)
        self.conn = sqlite3.connect(db)
        self.c  = self.conn.cursor()

        # variables
        self.tup_prop = ("esri", "mapinfo", "arc", "geoconcept", "starapic", "1spatial", "business geographic", "fme", "intragéo", "intergraph")
        self.tup_opso = ("qgis", "quantumgis", "gvsig", "grass", "talend", "geokettle", "udig", "otb", "postgresql", "postgis")

        # extraction des types de contrats
        tr_contrats = threading.Thread(target=self.parse_contrats,
                                       args=(liste_identifiants_offre, self.c))
        tr_contrats.daemon = True
        tr_contrats.run()

        # # extraction des lieux des offres
        # tr_lieux = threading.Thread(target=self.parse_lieux,
        #                             args=(liste_identifiants_offre, self.c))
        # tr_lieux.daemon = True
        # tr_lieux.run()

        # extraction des logiciels
        tr_techno = threading.Thread(target=self.parse_technos,
                                       args=(liste_identifiants_offre, self.c))
        tr_techno.daemon = True
        tr_techno.run()

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
        # end of function
        # self.manage_connection(2)
        return li_id


    # def parse_lieux(self, li_id, db_cursor):
    #     """ extraction des lieux des offres """
    #     for offre in li_id:
    #         db_cursor.execute("SELECT title FROM georezo WHERE id = " + str(offre))
    #         #c.execute("SELECT title FROM georezo WHERE id = ?", str(offre))
    #         titre = db_cursor.fetchone()
    #         contrat = re.findall(u'[0-9]{3}'
    #         # insertion
    #         if contrat[0:3].lower() == 'cdi':
    #             db_cursor.execute("INSERT INTO lieux VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre), 1,0,0,0,0,0,0,0,0,""))
    #         elif contrat[0:3].lower() == 'cdd':
    #             db_cursor.execute("INSERT INTO lieux VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0, 1,0,0,0,0,0,0,0,""))
    #         elif "fpt" in contrat.lower():
    #             db_cursor.execute("INSERT INTO lieux VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0, 1,0,0,0,0,0,0,""))
    #         elif contrat.lower() == 'stage':
    #             db_cursor.execute("INSERT INTO lieux VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0,0, 1,0,0,0,0,0,""))
    #         elif "appr" in contrat.lower():
    #             s


    #         # Save (commit) the changes
    #         self.manage_connection(1)
    #     # end of function
    #     self.manage_connection(2)
    #     return li_id


    def parse_technos(self, li_id, db_cursor):
        """ extraction des logiciels cités dans l'offre """
        for offre in li_id:
            db_cursor.execute("SELECT content FROM georezo WHERE id = " + str(offre))
            content = db_cursor.fetchone()
            content = self.remove_tags(content[0])

            if any(prop in content for prop in self.tup_prop):
                # print("Ciel ! un logiciel propriétaire !")
                db_cursor.execute("INSERT INTO logiciels VALUES (?,?,?,?,?,?,?)", (str(offre), 1,0,0,0,0,0))
            elif any(prop in content for prop in self.tup_opso):
                # print("Cool ! Un logiciel libre !")
                db_cursor.execute("INSERT INTO logiciels VALUES (?,?,?,?,?,?,?)", (str(offre), 0,1,0,0,0,0))


            else:
                pass




            # Save (commit) the changes
            self.manage_connection(1)
        # end of function
        self.manage_connection(2)
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
    from os import path, getcwd
    import sqlite3
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

