# -*- coding: UTF-8 -*-
#!/usr/bin/env python

#------------------------------------------------------------------------------
# Name:         Analyseur (or Analizer in English)
# Purpose:      Analyzes the offers published on GeoRezo, extracts and formats
#               interesting informations: contracts types, date, etc.
#
# Authors:      pvernier (https://github.com/pvernier)
#               & Guts (https://github.com/Guts)
#
# Python:       3.4.x
# Created:      01/05/2014
# Updated:      03/11/2014
#
# Licence:      GPL 3
#------------------------------------------------------------------------------

###############################################################################
########### Libraries #############
###################################

# Standard library
from os import path
import re


# third party libraries
import nltk
from nltk.corpus import stopwords



annonce = "<p>Société : PROXISERVE<br />Lieu : Saint-Herblain (44)<br />Contrat : CDD&nbsp; 6 mois, évolutif en CDI<br />A pourvoir : Avant juillet 2014<br />Statut : ETAM<br />Formation : Niveau Bac + 2/3<br />Domaine :&nbsp; &nbsp; Bureau d&#8217;étude <br />Rémunération : 23000&#8364; à 26000&#8364;<br /><br />Vous agissez en collaboration avec le chargé d&#8217;exploitation réseau gaz et intervenez pour le compte de la société, spécialiste de l&#8217;exploitation et de la maintenance des réseaux de distribution de gaz propane.<br /><br />Vous assumez les tâches suivantes : <br /><br />- Reporting technique client (Réalisation de cartographies, Réalisation des DOE, Traitement et saisie des surveillances)<br /><br />- Support technique travaux (Réalisation de plan projet, Préparation des travaux : DT / DICT...)<br /><br />- Reporting contractuel / réglementaire (Traitement et suivi des rapports d&#8217;urgence gaz, Vérification réglementaire de l'outillage spécifique...)<br /><br />Profil recherché : <br /><br />Vous êtes à l&#8217;aise avec l&#8217;outil informatique, vous maîtrisez à minima Autocad (connaissance des outils SIG est un plus). <br /><br />Vous vous adaptez aisément à l&#8217;environnement qui vous entoure et êtes prêt(e) à faire quelques déplacements pour des missions opérationnelles.<br /><br />De nature curieuse et persévérante, vous êtes également force de proposition. <br /><br />Vous savez vous adapter à des objectifs précis dans des délais imposés (rigueur, autonomie, et efficacité).<br /><br />Dynamique et impliqué(e), vous souhaitez vous investir dans une entreprise qui offre de véritables opportunités aux candidats motivés et investis dans leurs missions.<br /><br />Merci d&#8217;adresser votre candidature à : <br /><br />PROXISERVE - Direction régionale Ouest <br />A l&#8217;attention de Coralie BELLANGER<br />2 rue Duguay Trouin - 44813 SAINT-HERBLAIN<br />Ou par email à : cbellanger AT proxiserve.fr</p>"
annonce_clean1 = ""
contenu_final = ""

def parse_words(contenu):
    """
    Extraction of words mentioned into the offers. The goal is to perform
    a semantic analysis.
    It's based on NLTK: http://www.nltk.org

    li_id = list of offers'IDs to process
    db_cursor = connection cursor to the DB where to store extracted data
    """
    global annonce_clean1, contenu_final
    # get list of common French words to filter
    stop_fr = set(stopwords.words('french'))   # add specific French

    # custom list
    li_stop_custom = ('(', ')', '...', '.',':',';','/','nbsp','&','#',',','-',':',\
                      'http', 'img', 'br', 'amp', '<', '>', '%', 'border', '*', 'border=',
                      'les', 'leurs', '&', '#', '-', '+', ':', '.', ';', 'à', 'où', 'des',
                      ',', 'nbsp', 'De', 'et', 'en', '(', ')', 'pour')

    # list to store words OK
    li_words_ok = []
    # dictionary of words/frequency
    dict_words_frek = {}

    # basic clean of the content
    annonce_clean1 = remove_tags(contenu)
    annonce_clean1 = ''.join([i for i in annonce_clean1 if not i.isdigit()])
    # tokenizing and cleaning html tags
    # contenu = nltk.word_tokenize(nltk.clean_html(contenu))
    contenu_final = nltk.word_tokenize(annonce_clean1)
    # filtering
    for mot in contenu_final:
        if mot not in stop_fr and mot not in li_stop_custom and len(mot) > 2:
            li_words_ok.append(mot)
        else:
            pass

    print(li_words_ok)

    # calc words frequency
    for mot in li_words_ok:
        if mot in dict_words_frek:
            dict_words_frek[mot] = dict_words_frek.get(mot) + 1
        else:
            dict_words_frek[mot] = 1

    # end of function
    return annonce_clean1

def remove_tags(html_text):
    """
    very basic cleaner for HTML markups
    """
    try:
        text = ' '.join(ET.fromstring(html_text).itertext())
    except:
        TAG_RE = re.compile(r'<[^>]+>')
        return TAG_RE.sub(' ', html_text)
    # end of function
    return text.lower()


parse_words(annonce)

print(annonce_clean1)

print("\n\n")
print(contenu_final)

