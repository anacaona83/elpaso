El Paso
======

Statistiques dynamiques sur les offres d'emploi en géomatique publiées sur le forum francophone de géomatique [GeoRezo](http://georezo.net/forum/viewforum.php?id=10).
Pour tester : [serveur de démonstration](http://62.210.239.81:8443/contrats_exploit/)

## ToDoList

- [ ] camembert par mois et par type de contrat (@Guts)
- [ ] exemple de courbes selon temps [prénoms](http://dataaddict.fr/prenoms/)
- [ ] histogramme cumulatif et interactif : http://bl.ocks.org/mbostock/3886208
- [ ] représenter graphiquement les lieux (carte ?) et logiciels (bulles ?)
- [X] optimiser le html avec intégration de bootstrap (@pvernier)
- [ ] configuration serveur web (nginx)
- [ ] optimisation du cache pour les fichiers JSON
- [X] ajout des libraires JS en local (d3, bootstrap et jquery)
- [ ] mise en page globale (menu bandeau type BS)
- [ ] union des tables dans une seule BD (django et crawler)
- [X] migration vers PostgreSQL ? mieux vaut rester sur sqlite.
- [X] finaliser le script de récupération et d'insertion dans la BD

### Principe

### Phase récupération

1. jobs_georezo.py est croné 2 fois par jour
2. il check s'il y a des nouvelles offres publiées depuis son dernier passage
3. s'il y a des nouvelles offres :
4. il récupère les id des nouvelles offres
5. stocke les infos brutes dans la table georezo
6. lance les différentes fonctions/process/parsers en donnant en paramètre la liste des id des nouvelles offres

### Régler la tâche planifiée (cron)

=> 2 fois par jour, à 1h et 13h.
crontab -e puis ajouter :

```bash
0 1,13 * ~/elpaso/envs/env1/bin/python /elpaso/utils/jobs_georezo.py
```


# Base de données

## Structuration des tables

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

## Recréer la base de données

```sql
CREATE TABLE "autres" ("id" INTEGER PRIMARY KEY  NOT NULL  UNIQUE , "langue" VARCHAR NOT NULL );

CREATE TABLE "contrats" ("id" INTEGER PRIMARY KEY  NOT NULL ,"cdi" BOOL,"cdd" BOOL,"fpt" BOOL,"stage" BOOL,"apprentissage" BOOL,"vi" BOOL,"these" BOOL,"post_doc" BOOL,"mission" BOOL, "autres" VARCHAR);

CREATE TABLE "georezo" ("id" INTEGER PRIMARY KEY  NOT NULL  UNIQUE , "title" VARCHAR NOT NULL , "content" TEXT NOT NULL , "date_pub" DATETIME);

CREATE TABLE "lieux" ("id" INTEGER PRIMARY KEY  NOT NULL ,"lieu_lib" VARCHAR NOT NULL ,"lieu_type" INTEGER NOT NULL );

CREATE TABLE "logiciels" ("id" INTEGER PRIMARY KEY  NOT NULL , "proprietaire" BOOL, "libre" BOOL, "sgbd" BOOL, "programmation" BOOL, "web" BOOL, "cao_dao" BOOL);

CREATE TABLE "metiers" ("id" INTEGER PRIMARY KEY  NOT NULL ,"administrateur" BOOL DEFAULT (null) ,"cartographe" BOOL,"charge_etude" BOOL,"charge_mission" BOOL,"chef" BOOL,"geometre" BOOL,"ingenieur" BOOL,"responsable" BOOL,"sigiste" BOOL,"technicien" BOOL,"topographe" BOOL);
```
