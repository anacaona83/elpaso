# -*- coding: UTF-8 -*-
#!/usr/bin/env python

from __future__ import unicode_literals

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
from xml.etree import ElementTree as ET

import json


import data


db_path = u"C:/Users/julien.moura/Documents/GitHub/elpaso\elpaso.sqlite"

# connection to the DB
db = path.abspath(db_path)
conn = sqlite3.connect(db)
c = conn.cursor()


# c.execute('SELECT * FROM jobs_semantic_global \
#                    WHERE rowid=9967')
# row = c.fetchone()

# print row
# print type(row[0])


# print row[0].startswith(u"\u2022")

def remove_tags(html_text):
    """
    very basic cleaner for HTML markups
    """
    try:
        text = ' '.join(ET.fromstring(html_text).itertext())
    except:
        TAG_RE = re.compile(r'<[^>]+>')
        return TAG_RE.sub(' ', html_text)
    # end of function
    return text.lower()

# ######### SEMANTIQUE
# c.execute('SELECT occurrences, word, first_time, last_time \
#            FROM jobs_semantic_global \
#            ORDER BY occurrences DESC\
#            LIMIT 500')
# semantic_frek = c.fetchall()

# frequences = [{'word': t[1], 'size': t[0], 'firstime': t[2], 'lastime': t[3]}
# 			 for t in sorted(semantic_frek[0:499], reverse=True)]

# # print frequences

# with open('C:/Users/julien.moura/Documents/GitHub/d3-cloud/examples/mots_geomatique.json', 'w') as output:
#     json.dump(frequences, output, indent=4)


# ######### TECHNOLOGIES
# c.execute('SELECT occurrences, word, first_time, last_time \
#            FROM jobs_semantic_global \
#            ORDER BY occurrences DESC\
#            LIMIT 500')
# technos_types = c.fetchall()

# technos = [{'word': t[1], 'size': t[0], 'firstime': t[2], 'lastime': t[3]}
# 			 for t in sorted(technos_types, reverse=True)]

# # print frequences

# with open('C:/Users/julien.moura/Documents/GitHub/d3-cloud/examples/technos_global.json', 'w') as output:
#     json.dump(frequences, output, indent=4)


# test_big_list = range(0, 719)
# print(len(test_big_list))

# test_little_list = range(0,33)
# print(len(test_little_list))

# big_youhou = zip(*[iter(test_big_list)]*100)
# print(len(big_youhou))
# for partlist in big_youhou:
#     print(partlist)

# little_youhou = zip(*[iter(test_little_list)]*100)
# print(len(little_youhou))

# print(little_youhou)


# big_youpi = [test_big_list[i:i+100] for i  in range(0, len(test_big_list), 100)]
# print(big_youpi)





###### TESTING technos parser
c.execute("SELECT content FROM georezo WHERE id={0}".format(251130))
contenu = c.fetchone()
contenu = remove_tags(contenu[0])

try:
    print contenu
except UnicodeEncodeError:
    contenu = contenu.encode('utf8')

print(contenu)

li_values = [str(251130)]

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


print(li_values)
