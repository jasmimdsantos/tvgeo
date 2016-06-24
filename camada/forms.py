from django import forms
from leaflet.forms.widgets import LeafletWidget
from leaflet.forms.fields import MultiPolygonField, MultiLineStringField, PointField

class FrmLocal(forms.Form):

    descricao = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 4}))
    geojson = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}), required=False)
    poligono = MultiPolygonField(required=False)
    ponto = PointField(required=False)
    linha = MultiLineStringField(required=False)


    class Meta:
        fields = ('descricao ', 'geojson')
        widgets = {'poligono': LeafletWidget(),
                   'ponto': LeafletWidget(),
                   'linha': LeafletWidget()
                   }





