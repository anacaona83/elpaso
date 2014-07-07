# imports
from os import path
import re
import sqlite3


# db settings
db = path.abspath(r"elpaso.sqlite")
conn = sqlite3.connect(db)
c  = conn.cursor()


# get offers title
c.execute("SELECT title FROM georezo")
titres = c.fetchall()


# departments codes
tup_dpts = (1,2,3,4,5,6,7,8,9,10,\
 11,12,13,14,15,16,17,18,19,20,\
 21,22,23,24,25,26,27,28,29,30,\
 31,32,33,34,35,36,37,38,39,40,\
 41,42,43,44,45,46,47,48,49,50,\
 51,52,53,54,55,56,57,58,59,60,\
 61,62,63,64,65,66,67,68,69,70,\
 71,72,73,74,75,76,77,78,79,80,\
 81,82,83,84,85,86,87,88,89,90,\
 91,92,93,94,95,96,97,98,99,100,\
 101,"2A","2B",971,972,973,974,975)


for titre in titres:
    lieu_reg1 = re.findall("(([\d]{2} )|(2[abAB] ))", titre[0])
    print("========", titre[0], "\nreg1", lieu_reg1)
    lieu_reg2 = re.findall("(\()([0-9]+)(\))", titre[0])
    print("reg2", lieu_reg2)
    lieu_reg3 = re.findall("(2[AB]|[0-9]+)", titre[0])
    print("\nreg3", lieu_reg3, type(lieu_reg3))
