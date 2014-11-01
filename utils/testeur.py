# -*- coding: UTF-8 -*-
#!/usr/bin/env python

from os import path
import feedparser
import sqlite3


# Custom modules
from modules import analyseur
from modules import models
from modules import LogGuy

logger = LogGuy.Logyk()

# opening the log file
logger.config()

# DB connection settings
db = path.abspath(r"/home/pvernier/code/python/elpaso/elpaso.sqlite")
conn = sqlite3.connect(db)
c = conn.cursor()
# fetching the ID list
c.execute("SELECT id FROM georezo")
liste_input = [i[0] for i in c.fetchall()]


# analyseur.Analizer(liste_input)
models.Fillin(liste_input)

# mettre à jour les index
## CREATE UNIQUE INDEX "main"."idx_id" ON "logiciels" ("id" ASC)

# closing process
logger.append('<<<<<<<<<<<< El Paso finished without any issue ! >>>>>>>>>>>>>>>>>>>>>\n')