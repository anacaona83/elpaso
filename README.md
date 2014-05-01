El Paso
======

Statistiques dynamiques sur les offres d'emploi en géomatique publiées sur GeoRezo.



Régler la tâche planifiée (cron)
==
crontab -e puis ajouter :
# 2 fois par jour, à 1h et 13h.
0 1,13 * /elpaso/envs/env1/bin/python /elpaso/jobs_georezo.py
