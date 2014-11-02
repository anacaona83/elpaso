from django.db import models


class Contrat(models.Model):
    """ """
    id = models.IntegerField(primary_key=True, db_index=True)
    type = models.CharField(max_length=255)
    date_pub = models.DateTimeField()
    week_number = models.IntegerField()
    day_of_week = models.IntegerField()
    dept = models.CharField(max_length=3)
    country = models.CharField(max_length=50)

    # def __str__(self):
    #     return self.id


class Year(models.Model):
    """ """
    # specific fields for period
    year = models.IntegerField(db_index=True)
    # contrats types fields
    cdi = models.IntegerField(default=0)
    cdd = models.IntegerField(default=0)
    fpt = models.IntegerField(default=0)
    stage = models.IntegerField(default=0)
    apprentissage = models.IntegerField(default=0)
    vi = models.IntegerField(default=0)
    these = models.IntegerField(default=0)
    post_doc = models.IntegerField(default=0)
    mission = models.IntegerField(default=0)
    autre = models.IntegerField(default=0)
    # timestamp in milliseconds
    year_milsec = models.BigIntegerField()

    def __str__(self):
        return str(self.year)


class Month(models.Model):
    """ """
    # specific fields for period
    year = models.IntegerField(db_index=True)
    month = models.IntegerField(db_index=True)
    # contrats types fields
    cdi = models.IntegerField(default=0)
    cdd = models.IntegerField(default=0)
    fpt = models.IntegerField(default=0)
    stage = models.IntegerField(default=0)
    apprentissage = models.IntegerField(default=0)
    vi = models.IntegerField(default=0)
    these = models.IntegerField(default=0)
    post_doc = models.IntegerField(default=0)
    mission = models.IntegerField(default=0)
    autre = models.IntegerField(default=0)
    # timestamp in milliseconds
    month_milsec = models.BigIntegerField()

    def __str__(self):
        return str(self.month)


class Week(models.Model):
    """ """
    # specific fields for period
    year = models.IntegerField(db_index=True)
    week = models.IntegerField(db_index=True)
    first_day = models.DateTimeField(db_index=True)
        # contrats types fields
    cdi = models.IntegerField(default=0)
    cdd = models.IntegerField(default=0)
    fpt = models.IntegerField(default=0)
    stage = models.IntegerField(default=0)
    apprentissage = models.IntegerField(default=0)
    vi = models.IntegerField(default=0)
    these = models.IntegerField(default=0)
    post_doc = models.IntegerField(default=0)
    mission = models.IntegerField(default=0)
    autre = models.IntegerField(default=0)
    # timestamp in milliseconds
    week_milsec = models.BigIntegerField()

    def __str__(self):
        return str(self.week)
