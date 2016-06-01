from django.forms import ModelForm , Form
from .models import Quadro, QuadroItem
from django import forms

class QuadroForm(ModelForm):
    class Meta ():
        model = Quadro
        fields = ['descricao',]