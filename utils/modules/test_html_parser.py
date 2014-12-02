# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# from __future__ import unicode_literals

from os import path

import re

from urllib2 import urlopen

import bleach

import sqlite3


from bs4 import BeautifulSoup, NavigableString

def strip_tags(html, invalid_tags):
    soup = BeautifulSoup(html)

    for tag in soup.findAll(True):
        if tag.name in invalid_tags:
            s = ""

            for c in tag.contents:
                if not isinstance(c, NavigableString):
                    c = strip_tags(unicode(c), invalid_tags)
                s += unicode(c)

            tag.replaceWith(s)

    return soup

html = "<p>Good, <b>bad</b>, and <i>ug<b>l</b><u>y</u></i></p>"
invalid_tags = ['b', 'i', 'u']
print(strip_tags(html, invalid_tags))

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


# connection to the DB
db = path.abspath(r"../../elpaso.sqlite")
conn = sqlite3.connect(db)
db_cursor = conn.cursor()

# get content
db_cursor.execute("SELECT content FROM georezo WHERE {0}".format(str(259412)))
contenu = db_cursor.fetchone()
print(type(contenu[0]))
print(contenu[0].encode('utf8'))

contenu = contenu[0].encode('utf8')



print('\n=========================== BASIC CLEANER\n')

cleaned = remove_tags(contenu.decode('utf8'))
print(cleaned)

print('\n=========================== BEAUTIFUL SOUP\n')

# soup = BeautifulSoup.BeautifulSoup(contenu[0].encode('latin1'))
# print(soup)


print('\n=========================== BLEACH \n')

print(bleach.clean(contenu[0]).encode('UTF-8'))
