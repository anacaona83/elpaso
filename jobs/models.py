from django.db import models


class Contrat(models.Model):
    """
    table to store jobs offers per contracts types
    """
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
    """
    table to store jobs offers per years
    """
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
    """
    table to store jobs offers per month
    """
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
    """
    table to store jobs offers per week
    """
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


class Places_Global(models.Model):
    """
    table to store jobs offers per places mentioned
    """
    id = models.IntegerField(primary_key=True, db_index=True)
    libelle = models.CharField(max_length=200)
    niveau_territorial = models.IntegerField(default=0)
    logs = models.CharField(max_length=200)

    # end
    def __str__(self):
        return str(self.places_global)


class Technos_Types(models.Model):
    """
    table to store jobs offers per type of technology required
    """
    id = models.IntegerField(primary_key=True, db_index=True)
    proprietaire = models.IntegerField(default=0)
    libre = models.IntegerField(default=0)
    sgbd = models.IntegerField(default=0)
    programmation = models.IntegerField(default=0)
    web = models.IntegerField(default=0)
    cao_dao = models.IntegerField(default=0)
    teledec = models.IntegerField(default=0)
    autres = models.CharField(max_length=100)

    # end
    def __str__(self):
        return str(self.technos_types)


class Semantic_Global(models.Model):
    """
    table to store words used in jobs offers to perform semantic analysis
    """
    mot = models.CharField(max_length=200, db_index=True)
    occurrences = models.IntegerField(default=0)    # frequency
    first_time = models.DateTimeField()
    last_time = models.DateTimeField()

    # end
    def __str__(self):
        return str(self.semantic_global)
