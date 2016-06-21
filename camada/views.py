from django.shortcuts import render
from . import  models

# Create your views here.
# add to the top
from .forms import FrmLocal
import json
from geomet import wkt


# add to your views
def local(request):
    if request.POST:
        form = FrmLocal(request.POST)
        if form.is_valid():
            print(request.POST['poligono'])
            form_descricao = request.POST['descricao']

            if not request.POST['geojson']:
                wktexto = request.POST['poligono']
                geometria = json.loads(request.POST['poligono'])
            else:
                data = json.loads(request.POST['geojson'])
                geometria = data['features'][0]['geometry']
                wktexto = wkt.dumps(geometria, decimals=4)

            regLocal = models.Local(descricao=form_descricao)
            regLocal.save()

            if geometria['type'] == "MultiPolygon":
                reg = models.Poligono(local_FK=regLocal, campo=wktexto)
                reg.save()
    else:
        form = FrmLocal()

    return render(request, 'camada/frmlLocal.html', {'form': form, })