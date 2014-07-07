from django.contrib import admin
from jobs.models import Contrat

class ContratAdmin(admin.ModelAdmin):
    pass
admin.site.register(Contrat, ContratAdmin)