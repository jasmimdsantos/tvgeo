from django.contrib import admin

from .models import  *

from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

# Register your models here.
admin.site.register(Local)
admin.site.register(Ponto, LeafletGeoAdmin)
admin.site.register(Poligono, LeafletGeoAdmin)