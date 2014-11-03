# -*- coding: UTF-8 -*-
#!/usr/bin/env python

#------------------------------------------------------------------------------
# Name:         Jobs from GeoRezo
# Purpose:      RSS parser of GeoRezo jobs forum to store offers into the
#               database. It's usually launched by a cron, twice a day.
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
import feedparser
import sqlite3

# Custom modules
from modules import analyseur
from modules import models
from modules import LogGuy

###############################################################################
########## Main program ###########
###################################

## LOG
# get the logger object
logger = LogGuy.Logyk()

# opening the log file
logger.config()

## DB
conn = sqlite3.connect(path.abspath(r'../elpaso.sqlite'))
c = conn.cursor()
logger.append("Connected to the database")

## PARSING
# Get the id of the last offer parsed
with open(path.abspath(r'last_id_georezo.txt'), 'r') as fichier:
    last_id = int(fichier.readline())
logger.append("Read ID of the last update")

# RSS parser
feed = feedparser.parse('http://georezo.net/extern.php?fid=10')
logger.append("Parser created")

# list to store offers IDs
li_id = []

# reset offers counter
compteur = 0

# looping on feed entries
for entry in feed.entries:
    # get the ID cleaning 'link' markup
    job_id = int(entry.id.split('#')[1].lstrip('p'))

    # first offer parsed is the last published, so the biggest ID. Put the ID in
    # the text file dedicated.
    if feed.entries.index(entry) == 0:
        with open(path.abspath(r'last_id_georezo.txt'), 'w') as fichier:
            fichier.write(str(job_id))
    else:
        pass

    # if the entry's ID is greater than ID stored in the file, that means
    # the offer is more recent and has not been processed yet.
    if job_id > last_id:
        try:
            with conn:
                #  storing the offer into the DB
                c.execute("INSERT INTO georezo VALUES (?,?,?,?)", (str(job_id),
                                                                   entry.title,
                                                                   entry.summary,
                                                                   entry.published))
                # incrementing counter
                compteur += 1
                # adding the offer's ID to the list of new offers to process
                li_id.append(job_id)
        except sqlite3.IntegrityError:
            # in case of duplicated offer
            logger.append("Offer already exists: " + str(job_id))
            continue
    else:
        pass

# closing connection
conn.close()

# log the number of new offers processed
logger.append(str(compteur) + ' offers have been added !')

# if new offers => launch next processes
if compteur > 0:
    # log info
    logger.append("New offers IDs: " + str(li_id))
    # analyzing offers
    analyseur.Analizer(li_id, path.abspath(r'../elpaso.sqlite'))
    # fillfulling the DB
    models.Fillin(li_id)
else:
    pass

# closing process
logger.append('<<<<<<<<< El Paso finished without any issue ! >>>>>>>>>>>>>>\n')
