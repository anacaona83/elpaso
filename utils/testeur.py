# -*- coding: UTF-8 -*-
#!/usr/bin/env python

from os import path, environ, listdir
import feedparser
import sqlite3
import sys

import time
from datetime import date as dt, datetime

# Custom modules
from modules import analyseur
from modules import models
from modules import LogGuy

sys.path.append('/home/pvernier/code/python/elpaso')
environ['DJANGO_SETTINGS_MODULE'] = 'elpaso.settings'
from jobs.models import Contrat
from jobs.models import Year
from jobs.models import Month
from jobs.models import Week


logger = LogGuy.Logyk()

# opening the log file
logger.config()

# empty tables to prevent conflicts
# Entry.objects.all().delete()

print("\nFin imports : {0}".format(datetime.now()))

# DB connection settings
db = path.abspath(r"/home/pvernier/code/python/elpaso/elpaso.sqlite")
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
conn.commit()

print("\nFin nettoyage tables en entrées : {0}".format(datetime.now()))

# fill input tables from georezo with analyseur
analyseur.Analizer(liste_input)

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
logger.append('<<<<<<<<<<<< Testing El Paso finished without any issue ! >>>>>>>>>>>>>>>>>>>>>\n')