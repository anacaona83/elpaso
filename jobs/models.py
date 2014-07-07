from django.db import models


class Contrat(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=255)
    date_pub = models.DateTimeField()
    week_number = models.IntegerField()
    day_of_week = models.IntegerField()

    # def __str__(self):
    #     return self.id