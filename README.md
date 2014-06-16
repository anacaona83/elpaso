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
- lieu_lib (si inconnu : "lieu inconnu")
- lieu_type (si inconnu : 99) : 
	+ 0 = continent
	+ 1 =  pays
	+ 2 = région
	+ 3 = département
	+ 4 = ville


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


# Recréer la BD

CREATE TABLE "autres" ("id" INTEGER PRIMARY KEY  NOT NULL  UNIQUE , "langue" VARCHAR NOT NULL );

CREATE TABLE "contrats" ("id" INTEGER PRIMARY KEY  NOT NULL ,"cdi" BOOL,"cdd" BOOL,"fpt" BOOL,"stage" BOOL,"apprentissage" BOOL,"vi" BOOL,"these" BOOL,"post_doc" BOOL,"mission" BOOL, "autres" VARCHAR);

CREATE TABLE "georezo" ("id" INTEGER PRIMARY KEY  NOT NULL  UNIQUE , "title" VARCHAR NOT NULL , "content" TEXT NOT NULL , "date_pub" DATETIME);

CREATE TABLE "lieux" ("id" INTEGER PRIMARY KEY  NOT NULL ,"lieu_lib" VARCHAR NOT NULL ,"lieu_type" INTEGER NOT NULL );

CREATE TABLE "logiciels" ("id" INTEGER PRIMARY KEY  NOT NULL , "proprietaire" BOOL, "libre" BOOL, "sgbd" BOOL, "programmation" BOOL, "web" BOOL, "cao_dao" BOOL);

CREATE TABLE "metiers" ("id" INTEGER PRIMARY KEY  NOT NULL ,"administrateur" BOOL DEFAULT (null) ,"cartographe" BOOL,"charge_etude" BOOL,"charge_mission" BOOL,"chef" BOOL,"geometre" BOOL,"ingenieur" BOOL,"responsable" BOOL,"sigiste" BOOL,"technicien" BOOL,"topographe" BOOL);