from django.contrib import admin
from .models import IncidentType, Incident

admin.site.register(IncidentType)
admin.site.register(Incident)
