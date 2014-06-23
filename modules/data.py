# -*- coding: UTF-8 -*-
#!/usr/bin/env python

# logiciels et langages propriétaires
tup_prop = ("esri", "mapinfo", "arc", "geoconcept", "starapic", "1spatial", "business geographic", "fme", \
	"intragéo", "intergraph", "apic", "aigle", "autocad", "autodesk", "google maps", "google earth", "dynmap")

# logiciels et langages open-source
tup_opso = ("qgis", "quantumgis", "gvsig", "grass", "talend", "geokettle", "udig", "otb", "postgresql", \
	"postgis", "monteverdi", "saga")

# logiciels et langages propriétaires
tup_sgbd = ("postgresql", "mysql", "oracle", "sql server", "postgis", "sde", "access", "mongodb")

# logiciels et langages propriétaires
tup_prog = ("python", "java", "C++", "r stats", "matlab", "spss", "html", "php", "ruby", "python", "java", \
	"javascript", "js", "css", "j2ee", "hibernate")

# logiciels et langages propriétaires
tup_web = ("html", "ajax", "php", "ruby", "python", "java", "webmapping", "mapnik", "javascript", "js", "css", \
	"wordpress", "openlayers", "leaflet", "django", "drupal", "joomla", "symphony", "angularjs", "nodejs", "web",\
	"geoserver", "mapserver", "server", "google maps", "dynmap")

# logiciels et langages propriétaires
tup_cdao = ("autocad", "autodesk", "micro station", "illustrator", "inkscape", "pao", "cao", "photoshop")

# logiciels et langages propriétaires
tup_teldec = ("e-cognition", "erdas", "imagine", "envi", "otb", "monteverdi", "photointerprétation", "photoshop")

# logiciels et langages propriétaires
tup_metier = ("cartographe", "cartographie", "topographe", "topographie", "sigiste", "dessinateur", \
	"administrateur", "développeur", "responsable", "chef de projet")

# logiciels et langages propriétaires
tup_pays = ('Afghanistan', 'Afrique du Sud', 'Albanie', 'Algérie', 'Allemagne', 'Andorre', 'Angola', 'Anguilla', 'Antarctique', \
	'Antigua-et-Barbuda', 'Antilles Néerlandaises', 'Arabie Saoudite', 'Argentine', 'Arménie', 'Aruba', 'Australie', 'Autriche', \
	'Azerbaïdjan', 'Bahamas', 'Bahreïn', 'Bangladesh', 'Barbade', 'Belgique', 'Belize', 'Bermudes', 'Bhoutan', 'Bolivie', \
	'Bosnie-Herzégovine', 'Botswana', 'Brunéi Darussalam', 'Brésil', 'Bulgarie', 'Burkina Faso', 'Burundi', 'Bélarus', 'Bénin',\
	'Cambodge', 'Cameroun', 'Québec', 'Canada', 'Cap-vert', 'Chili', 'Chine', 'Chypre', 'Colombie', 'Comores', 'Costa Rica', 'Croatie', 'Cuba', \
	"Côte d'Ivoire", 'Danemark', 'Djibouti', 'Dominique', 'El Salvador', 'Espagne', 'Estonie', 'Fidji', 'Finlande', 'France', \
	'Fédération de Russie', 'Russie', 'Gabon', 'Gambie', 'Ghana', 'Gibraltar', 'Grenade', 'Groenland', 'Grèce', 'Guadeloupe', \
	'Guam', 'Guatemala', 'Guinée', 'Guinée Équatoriale', 'Guinée-Bissau', 'Guyana', 'Guyane Française', 'Géorgie', \
	'Géorgie du Sud et les Îles Sandwich du Sud', 'Haïti', 'Honduras', 'Hong-Kong', 'Hongrie', 'Inde', 'Indonésie', 'Iraq', \
	'Irlande', 'Islande', 'Israël', 'Italie', 'Jamaïque', 'Japon', 'Jordanie', 'Kazakhstan', 'Kenya', 'Kirghizistan', 'Kiribati', \
	'Koweït', "L'ex-République Yougoslave de Macédoine", 'Lesotho', 'Lettonie', 'Liban', 'Libye', 'Libéria', 'Liechtenstein', \
	'Lituanie', 'Luxembourg', 'Macao', 'Madagascar', 'Malaisie', 'Malawi', 'Maldives', 'Mali', 'Malte', 'Maroc', 'Martinique', \
	'Maurice', 'Mauritanie', 'Mayotte', 'Mexique', 'Monaco', 'Mongolie', 'Montserrat', 'Mozambique', 'Myanmar', 'Namibie',\
	'Nauru', 'Nicaragua', 'Niger', 'Nigéria', 'Niué', 'Norvège', 'Nouvelle-Calédonie', 'Nouvelle-Zélande', 'Népal', 'Oman', \
	'Ouganda', 'Ouzbékistan', 'Pakistan', 'Palaos', 'Panama', 'Papouasie-Nouvelle-Guinée', 'Paraguay', 'Pays-Bas', 'Philippines', \
	'Pitcairn', 'Pologne', 'Polynésie Française', 'Porto Rico', 'Portugal', 'Pérou', 'Qatar', 'Roumanie', 'Royaume-Uni',\
	'Rwanda', 'République Arabe Syrienne', 'République Centrafricaine', 'République Dominicaine', \
	'République Démocratique Populaire Lao', 'République Démocratique du Congo', "République Islamique d'Iran",\
	'République Populaire Démocratique de Corée', 'République Tchèque', 'République de Corée', 'République de Moldova', \
	'République du Congo', 'République-Unie de Tanzanie', 'Réunion', 'Sahara Occidental', 'Saint-Kitts-et-Nevis', \
	'Saint-Marin', 'Saint-Pierre-et-Miquelon', 'Saint-Siège (état de la Cité du Vatican)', 'Saint-Vincent-et-les Grenadines', \
	'Sainte-Hélène', 'Sainte-Lucie', 'Samoa', 'Samoa Américaines', 'Sao Tomé-et-Principe', 'Serbie-et-Monténégro',\
	'Seychelles', 'Sierra Leone', 'Singapour', 'Slovaquie', 'Slovénie', 'Somalie', 'Soudan', 'Sri Lanka', 'Suisse', \
	'Suriname', 'Suède', 'Svalbard etÎle Jan Mayen', 'Swaziland', 'Sénégal', 'Tadjikistan', 'Taïwan', 'Tchad', \
	'Terres Australes Françaises', "Territoire Britannique de l'Océan Indien", 'Territoire Palestinien Occupé',\
	'Thaïlande', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinité-et-Tobago', 'Tunisie', 'Turkménistan', 'Turquie', \
	'Tuvalu', 'Ukraine', 'Uruguay', 'Vanuatu', 'Venezuela', 'Viet Nam', 'Wallis et Futuna', 'Yémen', 'Zambie',\
	'Zimbabwe', 'Égypte', 'Émirats Arabes Unis', 'Équateur', 'Érythrée', 'États Fédérés de Micronésie', 'États-Unis', \
	'Éthiopie', 'Île Bouvet', 'Île Christmas', 'Île Norfolk', 'Île de Man', 'Îles (malvinas) Falkland', \
	'Îles Caïmanes', 'Îles Cocos (Keeling)', 'Îles Cook', 'Îles Féroé', 'Îles Heard et Mcdonald', 'Îles Mariannes du Nord',\
	'Îles Marshall', 'Îles Mineures Éloignées des États-Unis', 'Îles Salomon', 'Îles Turks et Caïques', \
	'Îles Vierges Britanniques', 'Îles Vierges des États-Unis', 'Îles Åland')

# logiciels et langages propriétaires
tup_pays_pertinent = ('Belgique', 'Québec', 'Canada', 'Guadeloupe', 'Guyane', 'Martinique', 'Nouvelle-Calédonie', \
					  'Polynésie Française',  'Réunion', 'La Réunion', 'Saint-Pierre-et-Miquelon','Suisse')

# logiciels et langages propriétaires
tup_villes_fr100 = ("Paris", "Marseille", "Lyon", "Toulouse",  "Nice", "Nantes", "Strasbourg", "Montpellier", \
	"Bordeaux", "Lille", "Rennes", "Reims", "Le Havre", "Saint-Étienne", "Toulon", "Grenoble", "Dijon", "Angers", \
	"Le Mans", "Aix-en-Provence", "Brest", "Villeurbanne", "Nîmes", "Limoges", "Clermont-Ferrand", "Tours", "Amiens", \
	"Metz", "Besançon", "Perpignan", "Orléans", "Boulogne-Billancourt", "Mulhouse", "Caen", "Rouen", "Nancy",\
	"Saint-Denis", "Argenteuil", "Montreuil", "Roubaix", "Dunkerque", "Tourcoing", "Avignon", "Nanterre", \
	"Poitiers","Créteil", "Versailles", "Courbevoie", "Vitry-sur-Seine", "Pau", "Colombes", "Aulnay-sous-Bois", \
	"Asnières-sur-Seine", "Rueil-Malmaison", "Antibes", "La Rochelle","Saint-Maur-des-Fossés", "Champigny-sur-Marne", \
	"Calais", "Aubervilliers", "Cannes", "Béziers", "Bourges", "Saint-Nazaire", "Colmar", "Drancy", "Mérignac", "Ajaccio", \
	"Valence", "Quimper", "Issy-les-Moulineaux", "Noisy-le-Grand", "Levallois-Perret", "Villeneuve-d'Ascq", "Troyes", \
	"Antony", "Neuilly-sur-Seine", "La Seyne-sur-Mer", "Sarcelles", "Clichy", "Lorient", "Niort", "Pessac", "Vénissieux", \
	"Saint-Quentin", "Chambéry", "Ivry-sur-Seine", "Cergy", "Montauban", "Hyères", "Beauvais", "Cholet", "Bondy", \
	"Villejuif", "Vannes", "Maisons-Alfort", "Chelles", "Fontenay-sous-Bois", "Arles", "Fréjus")