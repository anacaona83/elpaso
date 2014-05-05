# -*- coding: UTF-8 -*-
#!/usr/bin/env python

#import os
import feedparser
import sqlite3


def extract(caracter):
    ''' Fonction qui extrait l'intitulé et le lieu en fonction
    d'un caractère de séparation '''
    t = entry.title.split(']')[1].split(caracter)
    # Si caracter est présent plus d'une fois
    if len(t) > 2:
        j = ''
        for e in t[:-1]:
            j = j + ' ' + e
        t = j.strip()
    else:
        t = t[0]
    l = entry.title.split(']')[1].split(caracter)[-1].strip()
    return t, l

# Si la BD n'existe pas, je la crée
# if 'elpaso.sqlite' not in os.listdir('.'):

#     conn = sqlite3.connect('bd_jobs_georezo.db')
#     c = conn.cursor()
#     c.execute('''CREATE TABLE jobs
#                  (id int, category text, title text,
#                   date timestamp, lieu text)''')
# # Sinon, je me connecte à la BD
# else:
conn = sqlite3.connect('/home/pvernier/code/python/elpaso/elpaso.sqlite')
c = conn.cursor()

# Ce fichier contient l'id de la dernière annonce traitée
fichier = open('/home/pvernier/code/python/elpaso/last_id_georezo.txt', 'r')
last_id = int(fichier.readline())
fichier.close()

# l'URL du flux RSS des annonces
d = feedparser.parse('http://georezo.net/extern.php?fid=10')

compteur = 0
for entry in d.entries:
    job_id = int(entry.id.split('#')[1].lstrip('p'))
    # La première annonce traitée est la dernière publiée, donc celle
    # qui a l'id le plus grand. Je mets cet id dans le fichier texte.
    if d.entries.index(entry) == 0:
        fichier = open('/home/pvernier/code/python/elpaso/last_id_georezo.txt', 'w')
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
        except:
            print(str(job_id))

conn.close()
# Affiche le nombre d'annonces insérées dans la BD
print(str(compteur) + ' annonces on été ajoutées')
