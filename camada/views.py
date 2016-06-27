from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Local
from .forms import FrmLocal
from django.template import RequestContext
from toolbox import sitetools
import json
from django.core.serializers.json import DjangoJSONEncoder
from geomet import wkt

def create_or_update_local(req):
    form_descricao = req['descricao']
    if 'local_id' in req:
        local_id = req['local_id']
    else:
        local_id = None

    if 'geojson' in req and req['geojson'] != '':
        data = json.loads(req['geojson'])
        geometria = data['features'][0]['geometry']
        #wktexto = wkt.dumps(geometria, decimals=4)
        wktexto = 'test'
        if geometria['type'] == "MultiPolygon":
            try:
                local_FK = Local.objects.get(pk=local_id)
                local_FK.descricao = form_descricao
                local_FK.poligono = wktexto
                local_FK.save()
            except Local.DoesNotExist or NameError:
                qry = Local(descricao=form_descricao, poligono=wktexto)
                qry.save()
                local_id = qry.id
        elif geometria['type'] == "MultiLineString":
            try:
                local_FK = Local.objects.get(pk=local_id)
                local_FK.descricao = form_descricao
                local_FK.linha = wktexto
                local_FK.save()
            except Local.DoesNotExist or NameError:
                qry = Local(descricao=form_descricao, linha=wktexto)
                qry.save()
                local_id = qry.id
        elif geometria['type'] == "Point":
            try:
                local_FK = Local.objects.get(pk=local_id)
                local_FK.descricao = form_descricao
                local_FK.ponto = wktexto
                local_FK.save()
            except Local.DoesNotExist or NameError:
                qry = Local(descricao=form_descricao, ponto=wktexto)
                qry.save()
                local_id = qry.id
    elif 'poligono' in req and req['poligono'] != '':
        poligono = req['poligono']
        try:
            local_FK = Local.objects.get(pk=local_id)
            local_FK.descricao = form_descricao
            local_FK.poligono = poligono
            local_FK.save()
        except Local.DoesNotExist or NameError:
            qry = Local(descricao=form_descricao, poligono=poligono)
            qry.save()
            local_id = qry.id

    elif 'linha' in req and req['linha'] != '':
        print("Linha")
        linha = req['linha']
        try:
            local_FK = Local.objects.get(pk=local_id)
            local_FK.descricao = form_descricao
            local_FK.linha = linha
            local_FK.save()
        except Local.DoesNotExist or NameError:
            qry = Local(descricao=form_descricao, linha=linha)
            qry.save()
            local_id = qry.id

    elif 'ponto' in req and req['ponto'] != '':
        print("Ponto")
        ponto = req['ponto']
        try:
            local_FK = Local.objects.get(pk=local_id)
            local_FK.descricao = form_descricao
            local_FK.ponto = ponto
            local_FK.save()
            print("Atualizou POnto")
        except Local.DoesNotExist or NameError:
            print("Criar Local")
            qry = Local(descricao=form_descricao, ponto=ponto)
            print(form_descricao)
            print(ponto)
            qry.save()
            local_id = qry.id

    return local_id

def api_editar_local(request):
    if request.POST:
        form = FrmLocal(request.POST)
        if form.is_valid():
            local_id = create_or_update_local(request.POST)
            return redirect('/camada/local/editar/'+str(local_id)+'/')



def criar_local(request):
    context = RequestContext(request)
    page = sitetools.sitemap(request.get_full_path()).context
    context.update(page)
    context['form'] = FrmLocal()
    return render(request, 'camada/frmlLocal.html', context)


def editar_local(request, id_local):
    context = RequestContext(request)
    page = sitetools.sitemap(request.get_full_path()).context
    context.update(page)

    local_FK = Local.objects.get(pk=id_local)

    initial_form = {}
    initial_form['descricao'] = local_FK.descricao
    initial_form['descricao'] = local_FK.descricao

    context['type'], initial_form[context['type']] = Local.campo.auto_get(instance=id_local)
    context['form'] = FrmLocal(initial=initial_form)
    context['local_id'] = id_local
    return render(request, 'camada/edit_local.html', context)

def remover_local(request, id_local):
    try:
        Local.objects.get(pk=id_local).delete()
        return redirect('/camada/local/criar/')
    except Local.DoesNotExist:
        return HttpResponse('Local não encontrado.', status=404)


def lista_local(request):
    context = RequestContext(request)
    page = sitetools.sitemap(request.get_full_path()).context
    context.update(page)

    return render(request, 'camada/lst_local.html', context)


def api_lista_local(request):
    qry = Local.objects.all()

    saidaR = []
    for item in qry:
        geometria, obj = Local.campo.auto_get(instance=item.id)
        mont = {'id': item.id,
                'descricao': item.descricao,
                'geometria': geometria.title()}
        saidaR.append(mont)

    saida = {"draw": 1,
             "recordsTotal": len(saidaR),
             "recordsFiltered": len(saidaR),
             "data": list(saidaR)}
    dados = json.dumps(saida, cls=DjangoJSONEncoder)
    return HttpResponse(dados, content_type='application/json')

def ver_local(request, id_local):
    local_FK = Local.objects.get(pk=id_local)
    geometria, obj = Local.campo.auto_get(instance=id_local)

    geojson = wkt.loads(obj)

    context = {
        'nome_mapa': local_FK.descricao,
        'obj': {
            'type': geojson['type'],
            'coordinates': geojson['coordinates']
            }
        }

    return render(request, 'camada/ver_local.html', context)