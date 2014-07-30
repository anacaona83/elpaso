from django.db import models


class Contrat(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=255)
    date_pub = models.DateTimeField()
    week_number = models.IntegerField()
    day_of_week = models.IntegerField()
    dept = models.CharField(max_length=3)
    country = models.CharField(max_length=50)

    # def __str__(self):
    #     return self.id


class Year(models.Model):
    year = models.IntegerField()
    cdi = models.IntegerField()
    cdd = models.IntegerField()
    fpt = models.IntegerField()
    stage = models.IntegerField()
    apprentissage = models.IntegerField()
    vi = models.IntegerField()
    these = models.IntegerField()
    post_doc = models.IntegerField()
    mission = models.IntegerField()
    autre = models.IntegerField()


# class Month(models.Model):
#     year = models.IntegerField()
#     month = models.IntegerField()
#     cdi = models.IntegerField()
#     cdd = models.IntegerField()
#     fpt = models.IntegerField()
#     stage = models.IntegerField()
#     apprentissage = models.IntegerField()
#     vi = models.IntegerField()
#     these = models.IntegerField()
#     post_doc = models.IntegerField()
#     mission = models.IntegerField()
#     autre = models.IntegerField()


# class Week(models.Model):
#     year = models.IntegerField()
#     month = models.IntegerField()
#     week = models.IntegerField()
#     first_day = models.DateTimeField()
#     cdi = models.IntegerField()
#     cdd = models.IntegerField()
#     fpt = models.IntegerField()
#     stage = models.IntegerField()
#     apprentissage = models.IntegerField()
#     vi = models.IntegerField()
#     these = models.IntegerField()
#     post_doc = models.IntegerField()
#     mission = models.IntegerField()
#     autre = models.IntegerField()
