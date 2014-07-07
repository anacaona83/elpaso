from os import path
import sqlite3
from datetime import datetime

db = path.abspath('elpaso.sqlite')
conn = sqlite3.connect(db)
c = conn.cursor()

# connexion à la BD Django
db_django = path.abspath('../django_projects/elpaso/db.sqlite3')
conn_django = sqlite3.connect(db_django)
c_django = conn_django.cursor()

c.execute("SELECT * FROM contrats")

contrats = c.fetchall()

for contrat in contrats:
    if contrat[1] == 1:
        # CDI
        type_contrat = 'cdi'

    elif contrat[2] == 1:
        type_contrat = 'cdd'

    elif contrat[3] == 1:
        type_contrat = 'fpt'

    elif contrat[4] == 1:
        type_contrat = 'stage'

    elif contrat[5] == 1:
        type_contrat = 'apprentissage'

    elif contrat[6] == 1:
        type_contrat = 'vi'

    elif contrat[7] == 1:
        type_contrat = 'these'

    elif contrat[8] == 1:
        type_contrat = 'post doc'

    elif contrat[9] == 1:
        type_contrat = 'mission'

    elif contrat[10]:
        type_contrat = 'autre'

    # Je récupère la date de l'annonce
    c.execute("SELECT date_pub FROM georezo WHERE id = " + str(contrat[0]))
    date = c.fetchone()
    
    date_object = datetime.strptime(date[0], "%a, %d %b %Y %H:%M:%S +0200")


    c_django.execute('INSERT INTO jobs_contrat VALUES \
                                      (?,?,?,?,?)', (str(contrat[0]),
                                      type_contrat, date_object,
                                      date_object.isocalendar()[1],
                                      date_object.isocalendar()[2]))
    conn_django.commit()
