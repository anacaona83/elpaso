import os
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
if 'bd_jobs_georezo.db' not in os.listdir('.'):

    conn = sqlite3.connect('bd_jobs_georezo.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE jobs
                 (id int, category text, title text,
                  date timestamp, lieu text)''')
# Sinon, je me connecte à la BD
else:
    conn = sqlite3.connect('bd_jobs_georezo.db')
    c = conn.cursor()

# Ce fichier contient l'id de la dernière annonce traitée
fichier = open('last_id_georezo.txt', 'r')
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
        fichier = open('last_id_georezo.txt', 'w')
        fichier.write(str(job_id))
        fichier.close()
    # Si l'id de l'annonce est supérieur à l'id du fichier, cela signifie
    # que l'annonce est plus récente et n'a pas encore été traitée
    if job_id > last_id:
        compteur += 1
        # Je ne garde que la catégorie, l'intitulé' et le lieu de l'annonce
        # qui se trouvent tous les 3 dans le titre (entry.title)
        # La catégorie est toujours (à vérifier) entre []
        # L'intitulé (ici titre) n'est pas important
        categorie = entry.title.split(']')[0].lstrip('[')
        # J'initialise le lieu ainsi au cas où il ne soit pas mentionné
        # dans l'annonce
        lieu = 'NULL'
        # A améliorer
        # Le lieu est souvent indiqué après '-', '–' ou ','
        if '–' in entry.title and '-' not in entry.title \
           and ',' not in entry.title:
            titre, lieu = extract('–')
        elif '-' in entry.title and '–' not in entry.title \
             and ',' not in entry.title:
            titre, lieu = extract('-')
        elif ',' in entry.title and '-' not in entry.title \
             and '–' not in entry.title:
            titre, lieu = extract(',')

        # J'insère les données dans la BD
        c.execute('INSERT INTO jobs VALUES (' + str(job_id) + ', "' +
                  categorie + '", "' + titre + '", "' + entry.published +
                  '", "' + lieu + '")')
        # Save (commit) the changes
        conn.commit()

conn.close()
# Affiche le nombre d'annonces insérées dans la BD
print(str(compteur) + ' annonces on été ajoutées')
