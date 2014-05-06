# -*- coding: UTF-8 -*-
#!/usr/bin/env python

from os import path
import sqlite3

# contrats

def parse_contrats(li_id):
    """ youhou """
    db = path.abspath("../elpaso.sqlite")
    db2 = "/home/geojulien/elpaso/elpaso.sqlite"
    conn = sqlite3.connect(db2)
    c = conn.cursor()
    print(db2)
    for offre in li_id:
        print(offre)
        c.execute("SELECT title FROM georezo WHERE id = " + str(offre))
        #c.execute("SELECT title FROM georezo WHERE id = ?", str(offre))
        titre = c.fetchone()
        print(titre[0])
        contrat = titre[0].split(']')[0].lstrip('[')
        # insertion
        if contrat[0:3].lower() == 'cdi':
            c.execute("INSERT INTO contrats VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre), 1,0,0,0,0,0,0,0,0,""))
        elif contrat[0:3].lower() == 'cdd':
            c.execute("INSERT INTO contrats VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0, 1,0,0,0,0,0,0,0,""))
        elif "fpt" in contrat.lower():
            c.execute("INSERT INTO contrats VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0, 1,0,0,0,0,0,0,""))
        elif contrat.lower() == 'stage':
            c.execute("INSERT INTO contrats VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0,0, 1,0,0,0,0,0,""))
        elif "appr" in contrat.lower():
            c.execute("INSERT INTO contrats VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0,0,0, 1,0,0,0,0,""))
        elif "vi" in contrat.lower() or "volontariat" in contrat.lower():
            c.execute("INSERT INTO contrats VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0,0,0,0, 1,0,0,0,""))
        elif contrat.lower() == "thèse":
            c.execute("INSERT INTO contrats VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0,0,0,0,0, 1,0,0,""))
        elif "post" in contrat.lower():
            c.execute("INSERT INTO contrats VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0,0,0,0,0,0, 1,0,""))
        elif "mission" in contrat.lower() or "interim" in contrat.lower():
            c.execute("INSERT INTO contrats VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0,0,0,0,0,0,0, 1,""))
        else:
            c.execute("INSERT INTO contrats VALUES (?,?,?,?,?,?,?,?,?,?,?)", (str(offre),0,0,0,0,0,0,0,0,0, contrat))

        # Save (commit) the changes
        conn.commit()
    # end of function
    conn.close()
    return li_id

##### stand-alone execution
##
##print(db)
##
##c.execute("SELECT id FROM georezo")
##liste_input = [i[0] for i in c.fetchall()]
###liste_input = c.fetchall()
##print(liste_input)
##parse_contrats(liste_input)
