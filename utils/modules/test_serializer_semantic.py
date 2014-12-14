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
import sqlite3

import json

db_path = u"../../elpaso.sqlite"

# connection to the DB
db = path.abspath(db_path)
conn = sqlite3.connect(db)
c = conn.cursor()


c.execute('SELECT occurrences, word, first_time, last_time \
           FROM jobs_semantic_global \
           ORDER BY occurrences DESC\
           LIMIT 250')
semantic_frek = c.fetchall()

frequences = [{'word': t[1], 'occurs': t[0], 'firstime': t[2], 'lastime': t[3]}
              for t in sorted(semantic_frek, reverse=True)]

with open('/home/pvernier/code/python/elpaso/static/json/mots_geomatique.json', 'w') as output:
    json.dump(frequences, output, indent=4)

