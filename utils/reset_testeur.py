# -*- coding: UTF-8 -*-
#!/usr/bin/env python

#------------------------------------------------------------------------------
# Name:         Test suite
# Purpose:      Make possible to test the parser and the crawler manually.
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
from os import path, environ
import sqlite3
import sys

from datetime import datetime

# Custom modules
from modules import analyseur
from modules import models
from modules import LogGuy

# Django specifics
sys.path.append(path.abspath(r'../'))
environ['DJANGO_SETTINGS_MODULE'] = 'elpaso.settings'
from jobs.models import Contrat
from jobs.models import Year
from jobs.models import Month
from jobs.models import Week
from jobs.models import Technos_Types
from jobs.models import Places_Global
from jobs.models import Semantic_Global

###############################################################################
########## Main program ###########
###################################
logger = LogGuy.Logyk()

# opening the log file
logger.config()

logger.append("Fin imports : {0}".format(datetime.now()))

# DB connection settings
db = path.abspath(r"../elpaso.sqlite")
conn = sqlite3.connect(db)
c = conn.cursor()

# fetching the ID list
c.execute("SELECT id FROM georezo")
liste_input = [i[0] for i in c.fetchall()]
conn.commit()

logger.append("Fin connexion BD et récupération Ids : {0}".format(datetime.now()))

# empty tables which are out of Django ORM
c.execute("DELETE FROM contrats;")
# c.execute("DELETE FROM lieux;")
# c.execute("DELETE FROM autres;")
# c.execute("DELETE FROM metiers;")
# c.execute("DELETE FROM logiciels;")
# c.execute("DELETE FROM semantique;")
conn.commit()

# # empty jobs_* tables
Contrat.objects.all().delete()
Year.objects.all().delete()
Month.objects.all().delete()
Week.objects.all().delete()
# Places_Global.objects.all().delete()
# Technos_Types.objects.all().delete()
# Semantic_Global.objects.all().delete()

logger.append("Fin nettoyage tables en entrée : {0}".format(datetime.now()))

# fill input tables from georezo with analyseur (except semantic)
# for performance matters, check the number of offers to process
logger.append(len(liste_input))
if len(liste_input) < 50:
    # analyseur.Analizer(liste_input, path.abspath(r'../elpaso.sqlite'))
    logger.append("Fin analyseur : {0}".format(datetime.now()))
    # loop on jobs list and get all dates per period
    models.Fillin(liste_input)
    conn.commit()
    logger.append("Fin répartition annonces par périodes : {0}".format(datetime.now()))
else:
    logger.append("Trop d'entrées : split de la liste")
    metalist_input = [liste_input[i:i + 50] for i in range(0, len(liste_input), 50)]
    for sublist in metalist_input:
        logger.append("annonces {0} à {1}".format(sublist[0], sublist[-1]))
        analyseur.Analizer(sublist,
		                   path.abspath(r'../elpaso.sqlite'),
		                   opt_types=1,
		                   opt_lieux=0,
		                   opt_technos=0,
		                   opt_metiers=0,
		                   opt_mots=0)
        conn.commit()
        logger.append("Fin analyseur des annonces {0} à {1} : {2}".format(sublist[0],
                                                                    sublist[-1],
                                                                    datetime.now()))
        # loop on jobs list and get all dates per period
        models.Fillin(sublist)
        logger.append("Fin répartition annonces par périodes : {0}".format(datetime.now()))

# analyseur.Analizer(liste_input,
#                    path.abspath(r'../elpaso.sqlite'),
#                    opt_types=0,
#                    opt_lieux=0,
#                    opt_technos=1,
#                    opt_metiers=0,
#                    opt_mots=0)

# update indexes
c.execute("PRAGMA auto_vacuum;")
conn.commit()
conn.close()

logger.append("Fin auto_vaccum : {0}".format(datetime.now()))



# closing process
logger.append('<<<<<<<<< Testing El Paso finished without any issue ! >>>>>>>>>>>\n')
