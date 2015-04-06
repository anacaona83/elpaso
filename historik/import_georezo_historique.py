# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from __future__ import (unicode_literals, print_function)
#------------------------------------------------------------------------------
# Name:         Test suite
# Purpose:      Make possible to test the parser and the crawler manually.
#
# Authors:      pvernier (https://github.com/pvernier)
#               & Guts (https://github.com/Guts)
#
# Python:       2.7.x
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
import time

import re

# 3rd party
import xlrd
import pytz


###############################################################################
########## Main program ###########
###################################

# timezone
paris_tz = pytz.timezone("Europe/Paris")

# log
log = open("import_logger.txt", "w")

xls_path = "BDD_JOB_v2.xls"

# opening
wbook_source = xlrd.open_workbook(xls_path, logfile=log)
sheet = wbook_source.sheet_by_index(0)

# DB connection settings
db = path.abspath(r"../elpaso.sqlite")
conn = sqlite3.connect(db)
c = conn.cursor()

# for col in range(sheet.ncols):
#     print(sheet.cell(0, col).value)
#     try:
#         print(sheet.cell(1, col).value)
#     except UnicodeEncodeError:
#         print(sheet.cell(1, col).value.encode('utf8'))


################################################################

for row in range(1, sheet.nrows):
    # parcours ligne par ligne
    idu = int(sheet.cell(row, 0).value)
    id_forum = int(sheet.cell(row, 1).value)
    id_rss = int(sheet.cell(row, 2).value)
    title = sheet.cell(row, 3).value
    contrat = sheet.cell(row, 6).value
    visits = int(sheet.cell(row, 7).value)
    dpt1 = sheet.cell(row, 8).value
    dpt2 = sheet.cell(row, 9).value
    region = sheet.cell(row, 10).value
    region_typ = sheet.cell(row, 11).value

    # récupérer et nettoyer le contenu de l'offre
    summary = sheet.cell(row, 13).value

    # enlever les astérisques
    rx = re.compile('\*+')
    summary = rx.sub(' ', summary).strip()

    # remplacer les doubles guillemets
    rx = re.compile('\Â«|Â»')
    summary = rx.sub(u'"', summary).strip()

    # enlever les copyright
    rx = re.compile('\Â®')
    summary = rx.sub('', summary).strip()

    # enlever les puces mal interprétées
    rx = re.compile('\â€¢')
    summary = rx.sub('', summary).strip()
    rx = re.compile('\â€”')
    summary = rx.sub('', summary).strip()
    rx = re.compile('\Â·')
    summary = rx.sub('', summary).strip()
    rx = re.compile('\Â°+')
    summary = rx.sub('', summary).strip()

    # enlever les lignes construites avec des underscores multiples
    rx = re.compile('_{2,}')
    summary = rx.sub('', summary).strip()

    # enlever les lignes construites avec des tirets multiples
    rx = re.compile('-{2,}')
    summary = rx.sub('', summary).strip()

    # enlever les codes html des caractères spéciaux mal interprétés
    rx = re.compile('&#+[0-9]{5}|;')
    summary = rx.sub(' ', summary).strip()
    rx = re.compile('â€¦')
    summary = rx.sub('', summary).strip()
    

    # enlever les balises html url et img
    rx = re.compile('\[[a-z]{3}\]|\[/[a-z]{3}\]')
    summary = rx.sub(' ', summary).strip()

    # remplacer les â
    rx = re.compile('\à¢+')
    summary = rx.sub(u'â', summary).strip()

    # remplacer les À
    rx = re.compile('\à€+')
    summary = rx.sub(u'À', summary).strip()

    # remplacer les ë
    rx = re.compile('\à«+')
    summary = rx.sub(u'ë', summary).strip()

    # remplacer les î
    rx = re.compile('\à®+')
    summary = rx.sub(u'î', summary).strip()

    # remplacer les ï
    rx = re.compile('\à¯')
    summary = rx.sub(u'ï', summary).strip()

    # remplacer les ô
    rx = re.compile('\à´+')
    summary = rx.sub(u'ô', summary).strip()

    # remplacer les œ
    rx = re.compile('\Å“')
    summary = rx.sub(u'œ', summary).strip()

    # remplacer les û
    rx = re.compile('\à»+')
    summary = rx.sub(u'û', summary).strip()

    # remplacer les ù
    rx = re.compile('\à¹')
    summary = rx.sub(u'ù', summary).strip()
    
    # remplacer les €
    rx = re.compile('\â‚¬+')
    summary = rx.sub(u' euros', summary).strip()

    # remplacer les ²
    rx = re.compile('\Â²+')
    summary = rx.sub(u'²', summary).strip()

    # remplacer les apostrophes mal interprétés
    rx = re.compile('d\?i|d\?I')
    summary = rx.sub(u"d'i", summary).strip()
    rx = re.compile('à¢â‚¬â„')
    summary = rx.sub(u"'", summary).strip()

    # try:
    #     print(summary)
    # except UnicodeEncodeError:
    #     print(summary.encode('UTF-8'))

    # récupérer la date
    cell_type = sheet.cell_type(row, 4)
    cell_value = sheet.cell_value(row, 4)
    if cell_type == xlrd.XL_CELL_DATE:
        dt_tuple = xlrd.xldate_as_tuple(cell_value, wbook_source.datemode)
        date_pub = datetime(
                            dt_tuple[0], dt_tuple[1], dt_tuple[2], 
                            dt_tuple[3], dt_tuple[4], dt_tuple[5]
                            )
        # ajouter fuseau horaire
        date_pub = paris_tz.localize(date_pub)
        published = time.strptime('{0} {1} {2} 04:44:44'.format(date_pub.year,
                                                                date_pub.month,
                                                                date_pub.day),
                                                                '%Y %m %d %H:%M:%S')
        if "2" in str(date_pub.utcoffset()):
            print('youhou')
            published = time.strftime("%a, %d %b %Y %H:%M:%S +0200", published)
        elif "1" in str(date_pub.utcoffset()):
            print('youpi')
            published = time.strftime("%a, %d %b %Y %H:%M:%S +0100", published)
        else:
            pass
    else:
        pass

    # # test si elle existe déjà dans El paso
    # if id_rss > 10265:
    #     print(u"Dans El Paso : ", title.encode("UTF-8"))
    #     print(u"Dernière annonce ajoutée : ".encode('UTF-8'), sheet.cell(row -1, 3).value.encode("UTF-8"))
    #     break
    # else:
    #     pass

    # insertion BDD
    c.execute("INSERT INTO historique VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (str(idu),
    																	  str(id_forum),
    																	  str(id_rss),
    																	  title,
                                                                          published,
                                                                          contrat,
                                                                          str(visits),
                                                                          dpt1,
                                                                          dpt2,
                                                                          region,
                                                                          region_typ,
                                                       					  summary))
    conn.commit()


conn.close()


################################################################

### to import into georezo table

# for row in range(1, sheet.nrows):
#     # parcours ligne par ligne
#     job_id = int(sheet.cell(row, 0).value)
#     title = sheet.cell(row, 3).value
#     summary = sheet.cell(row, 13).value
#     # récupérer la date
#     cell_type = sheet.cell_type(row, 4)
#     cell_value = sheet.cell_value(row, 4)
#     if cell_type == xlrd.XL_CELL_DATE:
#         dt_tuple = xlrd.xldate_as_tuple(cell_value, wbook_source.datemode)
#         date_pub = datetime(
#                             dt_tuple[0], dt_tuple[1], dt_tuple[2], 
#                             dt_tuple[3], dt_tuple[4], dt_tuple[5]
#                             )
#         # ajouter fuseau horaire
#         date_pub = paris_tz.localize(date_pub)
#         published = time.strptime('{0} {1} {2} 04:44:44'.format(date_pub.year,
#                                                                              date_pub.month,
#                                                                              date_pub.day),
#                                                                              '%Y %m %d %H:%M:%S')
#         if "2" in str(date_pub.utcoffset()):
#             print('youhou')
#             published = time.strftime("%a, %d %b %Y %H:%M:%S +0200", published)
#         elif "1" in str(date_pub.utcoffset()):
#             print('youpi')
#             published = time.strftime("%a, %d %b %Y %H:%M:%S +0100", published)
#         else:
#             pass
#     else:
#         pass

#     # test si elle existe déjà dans El paso
#     if job_id > 10265:
#         print(u"Dans El Paso : ", title.encode("UTF-8"))
#         print(u"Dernière annonce ajoutée : ".encode('UTF-8'), sheet.cell(row -1, 3).value.encode("UTF-8"))
#         break
#     else:
#         pass

#     # insertion BDD
#     c.execute("INSERT INTO georezo VALUES (?,?,?,?)", (str(job_id),
#                                                        title,
#                                                        summary,
#                                                        published))
#     conn.commit()


# conn.close()

# print(dir(date_pub))
# print(type(date_pub))
# print(date_pub.utcoffset())
# print(date_pub.tzinfo)
# print(date_pub.timetz())
print(published)
