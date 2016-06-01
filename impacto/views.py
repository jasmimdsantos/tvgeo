from django.shortcuts import render, redirect
from .models import Quadro, QuadroItem
from .forms import QuadroForm
from django.http import HttpResponse

def quadro(request):
    context = {}
    context['page'] = 'Quadro Questões'
    questoes = []

    quadro_FK = Quadro.objects.all()

    for quadro in quadro_FK:
        quest = {'titulo': quadro.descricao, 'id': quadro.id, 'respostas': []}
        respostas = []
        quadro_item_FK = QuadroItem.objects.filter(quadro_FK=quadro)
        for item in quadro_item_FK:
            resposta = {'msg': item.descricao, 'id': item.id}
            respostas.append(resposta)

        quest['respostas'] = respostas
        questoes.append(quest)

    form = QuadroForm()
    context['form'] = form
    context['questoes'] = questoes
    
    return render(request, 'impacto/quadro.html', context)
