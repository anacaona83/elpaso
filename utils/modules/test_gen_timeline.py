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

import json


db_path = u"..\..\elpaso.sqlite"

# connection to the DB
db = path.abspath(db_path)
conn = sqlite3.connect(db)
c = conn.cursor()


title = ""
datetime_pub = ""
type_contrat = ""
summary = ""
link = "http://georezo.net/forum/viewtopic.php?pid={0}".format(id)



# c.execute('SELECT * FROM jobs_semantic_global \
#                    WHERE rowid=9967')
# row = c.fetchone()



