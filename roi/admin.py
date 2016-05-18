from django.contrib import admin

from roi.models import DeteccaoChoices, CausaacidenteChoices,\
                            ExtratacidenteChoices, AtivagracidenteChoices,\
                            OutrasacidenteChoices,CausadorChoices,\
                            DanosVegetacoChoices, ROI

admin.site.register(DeteccaoChoices)
admin.site.register(CausaacidenteChoices)
admin.site.register(ExtratacidenteChoices)
admin.site.register(AtivagracidenteChoices)
admin.site.register(OutrasacidenteChoices)
admin.site.register(CausadorChoices)
admin.site.register(DanosVegetacoChoices)
admin.site.register(ROI)

