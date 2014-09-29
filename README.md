El Paso
==========

Statistiques dynamiques sur les offres d'emploi en géomatique publiées sur le forum francophone de géomatique [GeoRezo](http://georezo.net/forum/viewforum.php?id=10).
Pour tester : [serveur de démonstration](http://62.210.239.81/contrats_exploit/)

Pourquoi El Paso ? Depuis des temps immémoriaux, le choix d'un nom de projet informatique est cornélien. Né autour de fajitas et de rhum, le nom El Paso s'est imposé comme une évidence. Bien traduit, il représente le petit pas qui sépare un chercheur d'emploi d'un poste. Une simple offre, un simple pas... non, en fait, rien de tout cela, c'était juste parce-que les fajitas étaient bonnes !

![El Paso, logo](doc/OldElPaso_logo.jpg "Logo Old El Paso")


# ToDoList

- [ ] union des tables dans une seule BD (django et crawler)
- [ ] alimenter les tables par périodes
- [ ] exporter en json sous format : key : date, values: (liste valeurs par types de contrats)
- [ ] camembert par mois et par type de contrat (@Guts)
- [ ] exemple de courbes selon temps [prénoms](http://dataaddict.fr/prenoms/)
- [ ] graphique pour les types de contrats par semaines (http://nvd3.org/examples/stackedArea.html)
- [ ] graphique pour les types de contrats par mois (http://nvd3.org/examples/multiBar.html)
- [ ] histogramme cumulatif et interactif : http://bl.ocks.org/mbostock/3886208
- [ ] représenter graphiquement les lieux (carte ?) et logiciels (bulles ?)
- [X] optimiser le html avec intégration de bootstrap (@pvernier)
- [X] configuration serveur web (nginx)
- [ ] optimisation du cache pour les fichiers JSON
- [X] ajout des libraires JS en local (d3, bootstrap et jquery)
- [ ] mise en page globale (menu bandeau type BS)
- [X] migration vers PostgreSQL ? mieux vaut rester sur sqlite.
- [X] finaliser le script de récupération et d'insertion dans la BD
- [ ] Nombre de workers de gunicorn
- [ ] Différents logs serveur
- [X] installer et configurer NVD3 @Guts

# Principe

### Phase récupération

1. jobs_georezo.py est croné 2 fois par jour
2. il check s'il y a des nouvelles offres publiées depuis son dernier passage
3. s'il y a des nouvelles offres :
4. il récupère les id des nouvelles offres
5. stocke les infos brutes dans la table georezo
6. lance les différentes fonctions/process/parsers en donnant en paramètre la liste des id des nouvelles offres


### Phase consultation




# Installation et déploiement

Sur distribution Ubuntu Server 12.04 (Debian) avec git d'installé

## Base de données

### Structuration des tables

#### Table globale "lieux"

- id
- lieu_lib (si inconnu : "lieu inconnu")
- lieu_type (si inconnu : 99) : 
  + 0 = continent
  + 1 =  pays
  + 2 = région
  + 3 = département
  + 4 = ville


#### Table logiciels "contrats"

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


#### Structure table logiciels "logiciels"

* id
* proprietaire => Esri, MapInfo, Arc*, GeoConcept, StarApic, 1Spatial, Business Geographic, FME, Intragéo, Intergraph
* libre => QGIS, gvSIG, GRASS, Talend, GeoKettle, uDIG
* sgbd => PostgreSQL, MySQL, Oracle, SQL Server, PostGIS, SDE, Access
* programmation => Python, Java, C, C++, R,
* web => html, php, js, css, WordPress, OpenLayers, Leaflet, Django, Drupal, Joomla, Symphony, 
* cao/dao => autocad, Micro Station, Illustrator, Inkscape, PAO


#### Structure table "metiers"

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


#### Structure table "autres"

+ id
+ langue

### Commandes SQL initiales

```sql
CREATE TABLE "autres" ("id" INTEGER PRIMARY KEY  NOT NULL  UNIQUE , "langue" VARCHAR NOT NULL );

CREATE TABLE "contrats" ("id" INTEGER PRIMARY KEY  NOT NULL ,"cdi" BOOL,"cdd" BOOL,"fpt" BOOL,"stage" BOOL,"apprentissage" BOOL,"vi" BOOL,"these" BOOL,"post_doc" BOOL,"mission" BOOL, "autres" VARCHAR);

CREATE TABLE "georezo" ("id" INTEGER PRIMARY KEY  NOT NULL  UNIQUE , "title" VARCHAR NOT NULL , "content" TEXT NOT NULL , "date_pub" DATETIME);

CREATE TABLE "lieux" ("id" INTEGER PRIMARY KEY  NOT NULL ,"lieu_lib" VARCHAR NOT NULL ,"lieu_type" INTEGER NOT NULL );

CREATE TABLE "logiciels" ("id" INTEGER PRIMARY KEY  NOT NULL , "proprietaire" BOOL, "libre" BOOL, "sgbd" BOOL, "programmation" BOOL, "web" BOOL, "cao_dao" BOOL);

CREATE TABLE "metiers" ("id" INTEGER PRIMARY KEY  NOT NULL ,"administrateur" BOOL DEFAULT (null) ,"cartographe" BOOL,"charge_etude" BOOL,"charge_mission" BOOL,"chef" BOOL,"geometre" BOOL,"ingenieur" BOOL,"responsable" BOOL,"sigiste" BOOL,"technicien" BOOL,"topographe" BOOL);
```


## Installer Python 3.4

### Téléchargement / installation

Dans un terminal :

```bash
# dépendances
sudo apt-get install build-essential      # requis pour compiler
sudo apt-get install libsqlite3-dev       # librairie sqlite3
sudo apt-get install sqlite3              # client sqlite3 en ligne de commande
sudo apt-get install bzip2 libbz2-dev     # compression
sudo apt-get install libssl-dev openssl   # reqius par pip pour sécuriser les communications

# téléchargement des sources de Python 3.4.x
wget https://www.python.org/ftp/python/3.4.1/Python-3.4.1.tgz

# décompression de l'archive
tar xJf Python-3.4.0.tar.xz

# aller dans le dossier
cd Python-3.4.0/

# faire en sorte que Python 3.4.x s'installe à part de la version système
./configure --prefix=/opt/python3.4

# compilation/installation
make && sudo make install
```

### Configuration de .bashrc

```bash
# revenir à la racine système et ouvrir le fichier .bashrc
cd
sudo nano -c .bashrc

# dans l'éditeur du fichier rajouter :
alias python3="/opt/python3.4/bin/python3.4"
alias pyvenv="/opt/python3.4/bin/pyvenv-3.4"
alias pip3="/opt/python3.4/bin/pip3.4"

# sauvegarder (Ctrl + X) puis recharger 
source .bashrc
```

## Récupérer le projet et ses dépendances

```bash
# aller dans son dossier de travail
cd /home/$USER/python/
git clone https://github.com/pvernier/elpaso.git
```

## Environnement virtuel

Dans un terminal :

```bash
# aller dans son dossier de travail
cd /home/$USER/python/

# créer un nouvel environnement virtuel
pyvenv envs/env_elpaso

# Activer l'environnement virtuel
source ./envs/env_elpaso/bin/activate

# installer les modules
(env_elpaso) $ pip install pip install -r ../elpaso/requirements.txt
```

Quand le virtual env est activé pip représente pip3.4 et python, python3.4.x :

```bash
(env_elpaso) pvernier@sd-45564:~$ python
> Python 3.4.0 (default, Apr 28 2014, 12:53:21)
> [GCC 4.6.3] on linux
> Type "help", "copyright", "credits" or "license" for more information.
```

```python
(env_elpaso)$ python --version
Python 3.4.0
```

Pour désactiver :
`deactivate`

Bibliographie :

* http://askubuntu.com/questions/244544/how-do-i-install-python-3-3#244550
* https://stackoverflow.com/questions/22592686/compiling-python-3-4-is-not-copying-pip
* http://www.reddit.com/r/Python/comments/20xims/is_there_an_easy_way_to_install_python_34_on/


## Dépendances

Télécharger les librairies et modifier les chemins correspondants

* [Bootstrap 3.2.0](https://github.com/twbs/bootstrap/releases/download/v3.2.0/bootstrap-3.2.0-dist.zip)
* [D3.js](https://github.com/mbostock/d3/releases/download/v3.4.11/d3.zip)
* [NVD3](http://nvd3.org) : [nv.d3.js](https://raw.github.com/novus/nvd3/master/nv.d3.min.js) & [NVD3 CSS](https://raw.githubusercontent.com/novus/nvd3/master/src/nv.d3.css)

## Planifier la tâche planifiée (cron)

2 fois par jour, à 1h et 13h.

```bash
crontab -e 
# ajouter :
0 1,13 * * * /home/$USER/python/envs/env_elpaso/bin/python /home/$USER/python/elpaso/utils/jobs_georezo.py
```


## Configurer le serveur

Activer l'environnement virtuel et aller dans le dossier du projet
```
source envs/env_elpaso/bin/activate
cd elpaso/
```

### Gunicorn

```
# Installer gunicorn
pip install gunicorn

# Tester si gunicorn sert bien l'app django
gunicorn elpaso.wsgi:application --bind 62.210.239.81:8443

# Créer un dossier bin
mkdir bin

# copier le fichier chargé de démarrer gunicorn
cp doc/tpl_gunicorn_start bin/gunicorn_start

# personnaliser au besoin
nano -c doc/gunicorn_start

# rendre le fichier exécutable
sudo chmod u+x gunicorn_start

# tester (n'affiche parfois rien)
sudo su ./gunicorn_start
http://62.210.239.81:8443

```

### Supervisor

```bash
# installer supervisor
sudo apt-get install supervisor

# copier le fichier de configuration à partir du modèle
cp doc/tpl_elpaso.conf bin/elpaso.conf

# personnaliser au besoin
nano -c doc/elpaso.conf

# Créer le ficier de log
mkdir -p logs
touch logs/gunicorn_supervisor.log

# Demander à supervisor de relire le fichier de conf et d'actualiser
sudo supervisorctl reread
> elpaso: available

sudo supervisorctl update
> elpaso: added process group

# Vérifier le statut de l'app
sudo supervisorctl status elpaso
> elpaso                           RUNNING    pid 13473, uptime 0:00:04
```

#### IMPORTANT

Si le code django est modifié, il faut redémarrer supervisor pour voir les changements

```bash
sudo supervisorctl restart elpaso
> elpaso: stopped
> elpaso: started
```

### NGINX

```bash
# aller dans le dossier d'installation de nginx
cd /etc/ningx

# Créé un dossier sites-available et un dossier sites-enabled
sudo mkdir /etc/nginx/sites-available
sudo mkdir /etc/nginx/sites-enabled

# copier le fichier de configuration à partir du modèle
cp doc/tpl_nginx_elpaso.conf sites-available/elpaso.conf

# personnaliser au besoin
nano -c sites-available/elpaso.conf


# Créer un lien symbolique
sudo ln -s /etc/nginx/sites-available/elpaso /etc/nginx/sites-enabled/elpaso

# éditer la configuration ningx
sudo nano -c /etc/nginx/nginx.conf

# commenter :
include /etc/nginx/conf.d/*.conf;

# et ajouter :
include /etc/nginx/sites-enabled/*;

# Redémarrer le service
sudo service nginx restart
```

### Django

Faire en sorte que nginx serve les fichiers statiques de tous les dossiers **static** des apps et ceux listés dans _STATICFILES_DIRS_, pour les copier dans _STATIC_ROOT_.

```bash
cd /home/%USER/python/
source ./envs/env_elpaso/bin/activate
```

Dans settings.py je dois modifier ce qui concerne les fichiers static :

```python
# STATIC_ROOT n'est utile que pour la prod
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static_elpaso"),
    os.path.join(BASE_DIR, "../../js_libs"),
)
```

Lancer
`python manage.py collectstatic`


## Bibliographie

* http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/
* http://sametmax.com/nginx-en-reverse-proxy-gunicorn-pour-vos-apps-django/
* https://library.linode.com/web-servers/nginx/configuration/basic
* http://sametmax.com/comment-servir-les-fichiers-statiques-avec-django-en-dev-et-en-prod/
* http://makina-corpus.com/blog/metier/2014/reduire-le-poids-dun-geojson