El Paso
======

Statistiques dynamiques sur les offres d'emploi en géomatique publiées sur GeoRezo.



## Régler la tâche planifiée (cron)

crontab -e puis ajouter :
# 2 fois par jour, à 1h et 13h.
0 1,13 * /elpaso/envs/env1/bin/python /elpaso/jobs_georezo.py



## ToDolist
### Structure table globale "lieux" :
- id
- lieu_lib (si inconnu : "lieu inconu")
- lieu_type (si inconnu : 99)


### Structure table logiciels "contrats" :
+ id
+ cdi
+ cdd
+ stage
+ fpt
+ apprentissage
+ vi
+ these
+ post_doc
+ autres


### Structure table logiciels "logiciels" :
* id
* proprietaire => Esri, MapInfo, Arc*, GeoConcept, StarApic, 1Spatial, Business Geographic, FME, Intragéo, Intergraph
* libre => QGIS, gvSIG, GRASS, Talend, GeoKettle, uDIG
* sgbd => PostgreSQL, MySQL, Oracle, SQL Server, PostGIS, SDE, Access
* programmation => Python, Java, C, C++, R,
* web => html, php, js, css, WordPress, OpenLayers, Leaflet, Django, Drupal, Joomla, Symphony, 
* cao/dao => autocad, Micro Station, Illustrator, Inkscape, PAO


### Structure table "metiers" :
+ id
+ sigiste
+ cartographe
+ administrateur
+ geometre
+ topographe
+ ingenieur
+ technicien
+ charge_mission
+ charge_etude
+ responsable
+ chef


### Structure table "autres" :
+ id
+ langue



#### Principe
### Phase récupération
1. jobs_georezo.py est croné 2 fois par jour
2. il check s'il y a des nouvelles offres publiées depuis son dernier passage
3. s'il y a des nouvelles offres :
4. il récupère les id des nouvelles offres
5. stocke les infos brutes dans la table georezo
6. lance les différentes fonctions/process/parsers en donnant en paramètre la liste des id des nouvelles offres
