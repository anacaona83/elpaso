# -*- coding: UTF-8 -*-
#!/usr/bin/env python

from os import path
import feedparser
import sqlite3


# Custom modules
from modules import analyseur
from modules import LogGuy

logger = LogGuy.Logyk()

# opening the log file
logger.config()

# connexion à BD
conn = sqlite3.connect(path.abspath('elpaso.sqlite'))
c = conn.cursor()
logger.append("Connected to the database")

# Ce fichier contient l'id de la dernière annonce traitée
fichier = open(path.abspath('last_id_georezo.txt'), 'r')
last_id = int(fichier.readline())
fichier.close()
logger.append("Read ID of the last update")

# l'URL du flux RSS des annonces
d = feedparser.parse('http://georezo.net/extern.php?fid=10')
logger.append("Parser created")

# liste des identifiants des nouvelles offres
li_id = []

compteur = 0
for entry in d.entries:
    job_id = int(entry.id.split('#')[1].lstrip('p'))
    # La première annonce traitée est la dernière publiée, donc celle
    # qui a l'id le plus grand. Je mets cet id dans le fichier texte.
    if d.entries.index(entry) == 0:
        fichier = open(path.abspath('last_id_georezo.txt'), 'w')
        fichier.write(str(job_id))
        fichier.close()
    # Si l'id de l'annonce est supérieur à l'id du fichier, cela signifie
    # que l'annonce est plus récente et n'a pas encore été traitée
    if job_id > last_id:
        try:
            #  J'insère les données dans la BD
            c.execute("INSERT INTO georezo VALUES (?,?,?,?)", (str(job_id), entry.title, entry.summary, entry.published))
            # Save (commit) the changes
            conn.commit()
            compteur += 1
            li_id.append(job_id)
        except:
            logger.append("Offer already exists: " + str(job_id))

conn.close()
# Affiche le nombre d'annonces insérées dans la BD
logger.append(str(compteur) + ' offers have been added !')

# si de nouvelles annonces ont été insérées, alors on lance l'analyse
if compteur > 0:
    logger.append("New offers IDs: " + str(li_id))
    analyseur.Analizer(li_id)

# closing process
logger.append('<<<<<<<<<<<< El Paso finished without any issue ! >>>>>>>>>>>>>>>>>>>>>\n')