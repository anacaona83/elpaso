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

###############################################################################
########## Main program ###########
###################################
logger = LogGuy.Logyk()

# opening the log file
logger.config()

print("\nFin imports : {0}".format(datetime.now()))

# DB connection settings
db = path.abspath(r"../elpaso.sqlite")
conn = sqlite3.connect(db)
c = conn.cursor()

# fetching the ID list
c.execute("SELECT id FROM georezo")
liste_input = [i[0] for i in c.fetchall()]

print("\nFin connexion BD et récupération Ids : {0}".format(datetime.now()))

# empty tables which are out of Django ORM
c.execute("DELETE FROM contrats;")
c.execute("DELETE FROM lieux;")
c.execute("DELETE FROM autres;")
c.execute("DELETE FROM metiers;")
c.execute("DELETE FROM logiciels;")
c.execute("DELETE FROM semantique;")
conn.commit()

print("\nFin nettoyage tables en entrées : {0}".format(datetime.now()))

# fill input tables from georezo with analyseur
analyseur.Analizer(liste_input, path.abspath(r'../elpaso.sqlite'))

print("\nFin analyseur : {0}".format(datetime.now()))

# empty jobs_* tables
Contrat.objects.all().delete()
Year.objects.all().delete()
Month.objects.all().delete()
Week.objects.all().delete()

print("\nFin nettoyage tables sortie : {0}".format(datetime.now()))

# loop on jobs list and get all dates per period
models.Fillin(liste_input)

print("\nFin répartition annonces par périodes : {0}".format(datetime.now()))

# update indexes
c.execute("PRAGMA auto_vacuum;")

print("\nFin auto_vaccum : {0}".format(datetime.now()))

# closing process
logger.append('<<<<<<<<< Testing El Paso finished without any issue ! >>>>>>>>>>>\n')
