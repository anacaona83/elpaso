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
from os import path, environ
import sqlite3
import sys

import json

# Django specifics
sys.path.append('/home/pvernier/code/python/elpaso')
environ['DJANGO_SETTINGS_MODULE'] = 'elpaso.settings'
# from jobs.models import Technos_Types, Semantic_Global
# from django.db.models import Sum

#### SQLITE LIB
db_path = u"../../elpaso.sqlite"

# connection to the DB
db = path.abspath(db_path)
conn = sqlite3.connect(db)
c = conn.cursor()


c.execute('SELECT occurrences, word, first_time, last_time \
           FROM jobs_semantic_global \
           ORDER BY occurrences DESC\
           LIMIT 100')
semantic_frek = c.fetchall()
ratio = max([t[0] for t in sorted(semantic_frek, reverse=True)])/50
print(ratio)
print(t[0]/ratio)

frequences = [{'word': t[1], 'dim': t[0]/ratio, 'occurs': t[0], 'firstime': t[2], 'lastime': t[3]}
              for t in sorted(semantic_frek, reverse=True)]

with open('/home/pvernier/code/python/elpaso/static/json/mots_geomatique.json', 'w') as output:
    json.dump(frequences, output)

#### DJANGO LIB
# test_query = Semantic_Global.objects.values('occurrences', 'word', 'first_time', "last_time")\
#                             .order_by('-occurrences')[:250]
# print(len(test_query))
# print(test_query[1].get("word"))

# frequences = [{'word': item.get("word"),
#                'occurs': item.get("occurrences"),
#                'firstime': item.get("first_time"),
#                'lastime': item.get("last_time")}
#               for item in test_query]

# with open('/home/pvernier/code/python/elpaso/static/json/mots_geomatique_django.json', 'w') as output:
#     json.dump(frequences, output, indent=4)


# technos_get = Technos_Types.objects.aggregate(Sum('proprietaire'),
#                                                Sum('libre'),
#                                                Sum('sgbd'),
#                                                Sum('programmation'),
#                                                Sum('web'),
#                                                Sum('cao_dao'),
#                                                Sum('teledec'))

# technos_totaux = [{'label': item[0:-5],
#                    'value': technos_get.get(item)}
#                    for item in technos_get]

# with open('/home/pvernier/code/python/elpaso/static/json/technos_global.json', 'w') as output:
#     json.dump(technos_totaux, output)

