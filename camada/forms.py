from django import forms
from leaflet.forms.widgets import LeafletWidget
from leaflet.forms.fields import MultiPolygonField

class FrmLocal(forms.Form):

    descricao = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 4}))
    geojson = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 20}), required=False)
    poligono = MultiPolygonField()


class Meta:
    fields = ('geojson ', 'descricao')
    widgets = {'poligono': LeafletWidget()}





