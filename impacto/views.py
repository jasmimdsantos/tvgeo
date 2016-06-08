from django.shortcuts import render, redirect
from .models import Quadro, QuadroItem, Empresa, Projeto, FaseProjeto, ImpactoProjeto, Questionario, Diagnostico, TipoArea, Area, Impacto
from .forms import QuadroForm, Empresa_ProjetosForm, AreaForm, ImpactoProjetoForm , DiagnosticoForm
from django.http import HttpResponse
from django.template import RequestContext , loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from toolbox import sitetools
import json
from django.core.serializers.json import DjangoJSONEncoder

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

@login_required
def impacto(request):
    context = RequestContext(request)
    page = sitetools.sitemap ( request.get_full_path ( ) ).context
    context.update ( page )
    return render(request, "impacto/impacto.html", context)


def api_get_empresas ( request ):
    query = Empresa.objects.values('id', 'cnpj', 'nome',)
    saida = {"draw": 1 ,
             "recordsTotal": len ( query ) ,
             "recordsFiltered": len ( query ) ,
             "data": list ( query )}



    dados = json.dumps ( saida , cls=DjangoJSONEncoder )
    return HttpResponse ( dados , content_type='application/json' )


@login_required
def lst_empresas(request):
    context = RequestContext(request)
    page = sitetools.sitemap ( request.get_full_path ( ) ).context
    context.update ( page )
    return render(request, "impacto/lst_empresa.html", context)


def api_get_projetos( request, empresas ):
    if empresas == '0':
        query = Projeto.objects.values('id', 'cod_projeto', 'nome', 'status_FK__descricao', 'data_inicio', 'data_termino')
    else:
        query = Projeto.objects.filter(cliente_FK=empresas).values('id', 'cod_projeto', 'nome', 'status_FK__descricao', 'data_inicio', 'data_termino')
    saida = {"draw": 1 ,
             "recordsTotal": len ( query ) ,
             "recordsFiltered": len ( query ) ,
             "data": list ( query )}

    dados = json.dumps ( saida , cls=DjangoJSONEncoder )
    return HttpResponse ( dados , content_type='application/json' )

@csrf_exempt
@login_required
def lst_projetos(request):
    context = RequestContext(request)
    page = sitetools.sitemap ( request.get_full_path ( ) ).context
    context.update(page)
    context['empresa_id'] = 0
    if request.POST:
        if 'empresa' in request.POST:
            context['form'] = Empresa_ProjetosForm(initial={'empresas': request.POST['empresa']})
            context['empresa_id'] = request.POST['empresa']
        else:
            context['form'] = Empresa_ProjetosForm()

        if 'empresas' in request.POST:
            context['empresa_id'] = request.POST['empresas']
    else:
        context['form'] = Empresa_ProjetosForm()

    return render(request, "impacto/lst_projetos.html", context)


@login_required
def create_area(request, projeto):
    context = RequestContext(request)
    page = sitetools.sitemap ( request.get_full_path ( ) ).context
    context.update ( page )

    if request.POST:
        descricao = request.POST['descricao']
        obj = Area(descricao=descricao, projeto_FK_id=projeto)
        obj.save()
        return redirect('/impacto/perfil_projeto/'+projeto+"/")

    projeto_FK = Projeto.objects.get(pk=projeto)

    if not projeto_FK.data_termino:
        projeto_FK.data_termino = "Não Determinado"
    context['projeto'] = {'nome': projeto_FK.nome,
                          'id': projeto,
                          'descricao': projeto_FK.descricao,
                          'codigo': projeto_FK.cod_projeto,
                          'status': projeto_FK.status_FK,
                          'data_inicio': projeto_FK.data_inicio,
                          'data_termino': projeto_FK.data_termino}

    context['cliente'] = {'nome': projeto_FK.cliente_FK.nome, 'cnpj': projeto_FK.cliente_FK.cnpj}

    context['form'] = AreaForm()
    return render(request, "impacto/create_area.html", context)


@login_required
def create_impacto(request, projeto, faseprojeto):
    context = RequestContext(request)
    page = sitetools.sitemap ( request.get_full_path ( ) ).context
    context.update ( page )

    if request.POST:
        descricao = request.POST['descricao']
        areafk = request.POST['area_FK']
        tipoareafk = request.POST['tipo_area_FK']
        meiofk = request.POST['meio_FK']
        impactofk = request.POST['impacto_FK']
        obj = ImpactoProjeto(descricao=descricao,
                             fase_projeto_FK_id=faseprojeto,
                             area_FK_id=areafk,
                             tipo_area_FK_id=tipoareafk,
                             meio_FK_id=meiofk,
                             impacto_FK_id=impactofk)
        obj.save()
        return redirect('/impacto/perfil_projeto/'+projeto+"/")

    projeto_FK = Projeto.objects.get(pk=projeto)
    faseprojeto_FK = FaseProjeto.objects.get(pk=faseprojeto)

    if not projeto_FK.data_termino:
        projeto_FK.data_termino = "Não Determinado"

    context['projeto'] = {'nome': projeto_FK.nome,
                          'id': projeto,
                          'descricao': projeto_FK.descricao,
                          'codigo': projeto_FK.cod_projeto,
                          'status': projeto_FK.status_FK,
                          'data_inicio': projeto_FK.data_inicio,
                          'data_termino': projeto_FK.data_termino}

    context['fase'] = {'nome': faseprojeto_FK.get_descricao_display}

    context['cliente'] = {'nome': projeto_FK.cliente_FK.nome, 'cnpj': projeto_FK.cliente_FK.cnpj}

    form = ImpactoProjetoForm()
    form.fields['area_FK'].queryset = Area.objects.filter(projeto_FK_id=projeto)

    context['form'] = form
    context['faseprojeto'] = faseprojeto
    return render(request, "impacto/create_impacto.html", context)


@login_required
def create_diagnostico(request, projeto, faseprojeto):
    context = RequestContext(request)
    page = sitetools.sitemap ( request.get_full_path ( ) ).context
    context.update ( page )

    if request.POST:
        descricao = request.POST['descricao']
        areafk = request.POST['area_FK']
        tipoareafk = request.POST['tipo_area_FK']
        meiofk = request.POST['meio_FK']
        obj = Diagnostico(descricao=descricao,
                             fase_projeto_FK_id=faseprojeto,
                             area_FK_id=areafk,
                             tipo_area_FK_id=tipoareafk,
                             meio_FK_id=meiofk)
        obj.save()
        return redirect('/impacto/perfil_projeto/'+projeto+"/")

    projeto_FK = Projeto.objects.get(pk=projeto)
    faseprojeto_FK = FaseProjeto.objects.get(pk=faseprojeto)

    if not projeto_FK.data_termino:
        projeto_FK.data_termino = "Não Determinado"

    context['projeto'] = {'nome': projeto_FK.nome,
                          'id': projeto,
                          'descricao': projeto_FK.descricao,
                          'codigo': projeto_FK.cod_projeto,
                          'status': projeto_FK.status_FK,
                          'data_inicio': projeto_FK.data_inicio,
                          'data_termino': projeto_FK.data_termino}

    context['fase'] = {'nome': faseprojeto_FK.get_descricao_display}

    context['cliente'] = {'nome': projeto_FK.cliente_FK.nome, 'cnpj': projeto_FK.cliente_FK.cnpj}

    context['form'] = DiagnosticoForm()
    context['faseprojeto'] = faseprojeto
    return render(request, "impacto/create_diagnostico.html", context)


@login_required
def perfil_projeto(request, projeto):
    context = RequestContext(request)
    page = sitetools.sitemap ( request.get_full_path ( ) ).context
    context.update(page)
    projeto_FK = Projeto.objects.get(pk=projeto)
    cliente_FK = Empresa.objects.get(pk=projeto_FK.cliente_FK_id)
    if not projeto_FK.data_termino:
        projeto_FK.data_termino = "Não Determinado"

    context['cliente'] = {'nome': cliente_FK.nome, 'cnpj': cliente_FK.cnpj}
    context['projeto'] = {'nome': projeto_FK.nome,
                          'id': projeto_FK.id,
                          'descricao': projeto_FK.descricao,
                          'codigo': projeto_FK.cod_projeto,
                          'status': projeto_FK.status_FK,
                          'data_inicio': projeto_FK.data_inicio,
                          'data_termino': projeto_FK.data_termino}

    areas_FK = Area.objects.filter(projeto_FK_id=projeto)
    if areas_FK:
        context['areas'] = {'is_true': True, 'content': areas_FK}

    context['fase'] = {'P': {}, 'O': {}, 'I': {}, 'F': {}}
    faseprojeto_FK = FaseProjeto.objects.filter(projeto_FK_id=projeto)

    for item in faseprojeto_FK:
        impactoprojeto_FK = ImpactoProjeto.objects.filter(fase_projeto_FK=item.id).order_by('-meio_FK_id')
        diagnostico_FK = Diagnostico.objects.filter(fase_projeto_FK_id=item.id).order_by('-meio_FK_id')
        fase = context['fase']
        impactos = fase[str(item.descricao)] = {'id': item.id, 'content': {'impacto': '', 'diagnostico': ''}}
        impactos['content']['impacto'] = impactoprojeto_FK
        impactos['content']['diagnostico'] = diagnostico_FK

    return render(request, "impacto/perfil_projeto.html", context)


@login_required
def view_impacto(request, impacto):
    context = RequestContext(request)
    page = sitetools.sitemap(request.get_full_path()).context
    context.update(page)

    impacto_FK = Impacto.objects.get(pk=impacto)
    context['impacto'] = impacto_FK

    return render(request, "impacto/view_impacto.html", context)

@login_required
def edit_area(request, area):
    context = RequestContext(request)
    page = sitetools.sitemap(request.get_full_path()).context
    context.update(page)

    area_FK = Area.objects.get(pk=area)
    projeto_FK = Projeto.objects.get(pk=area_FK.projeto_FK_id)

    if request.POST:
        descricao = request.POST['descricao']
        obj = Area.objects.get(pk=area)
        obj.descricao = descricao
        obj.save()
        return redirect('/impacto/perfil_projeto/'+str(area_FK.projeto_FK_id)+"/")

    if not projeto_FK.data_termino:
        projeto_FK.data_termino = "Não Determinado"
    context['projeto'] = {'nome': projeto_FK.nome,
                          'id': projeto_FK.id,
                          'descricao': projeto_FK.descricao,
                          'codigo': projeto_FK.cod_projeto,
                          'status': projeto_FK.status_FK,
                          'data_inicio': projeto_FK.data_inicio,
                          'data_termino': projeto_FK.data_termino}

    context['cliente'] = {'nome': projeto_FK.cliente_FK.nome, 'cnpj': projeto_FK.cliente_FK.cnpj}
    context['area_id'] = area_FK.id
    context['form'] = AreaForm(instance=area_FK)

    return render(request, "impacto/edit_area.html", context)

@login_required
def edit_impacto_proj(request, impacto):
    context = RequestContext(request)
    page = sitetools.sitemap(request.get_full_path()).context
    context.update(page)

    impactoProj_FK = ImpactoProjeto.objects.get(pk=impacto)
    projeto_FK = impactoProj_FK.fase_projeto_FK.projeto_FK
    projeto_FK = Projeto.objects.get(pk=projeto_FK.id)

    if request.POST:
        descricaoForm = request.POST['descricao']
        meioForm = request.POST['meio_FK']
        tipo_areaForm = request.POST['tipo_area_FK']
        impactoForm = request.POST['impacto_FK']
        areaForm = request.POST['area_FK']
        obj = ImpactoProjeto.objects.get(pk=impacto)
        obj.descricao = descricaoForm
        obj.meio_FK_id = meioForm
        obj.tipo_area_FK_id = tipo_areaForm
        obj.impacto_FK_id = impactoForm
        obj.area_FK_id = areaForm
        obj.save()
        return redirect('/impacto/perfil_projeto/'+str(projeto_FK.id)+"/")

    if not projeto_FK.data_termino:
        projeto_FK.data_termino = "Não Determinado"

    context['projeto'] = {'nome': projeto_FK.nome,
                          'id': projeto_FK.id,
                          'descricao': projeto_FK.descricao,
                          'codigo': projeto_FK.cod_projeto,
                          'status': projeto_FK.status_FK,
                          'data_inicio': projeto_FK.data_inicio,
                          'data_termino': projeto_FK.data_termino}

    context['cliente'] = {'nome': projeto_FK.cliente_FK.nome, 'cnpj': projeto_FK.cliente_FK.cnpj}
    context['impacto_id'] = impacto
    context['fase'] = {'nome': impactoProj_FK.fase_projeto_FK.get_descricao_display}
    context['form'] = ImpactoProjetoForm(instance=impactoProj_FK)

    return render(request, "impacto/edit_impacto_projeto.html", context)

@login_required
def edit_diagnostico(request, diagnostico):
    context = RequestContext(request)
    page = sitetools.sitemap(request.get_full_path()).context
    context.update(page)

    diagnostico_FK = Diagnostico.objects.get(pk=diagnostico)
    projeto_FK = diagnostico_FK.fase_projeto_FK.projeto_FK
    projeto_FK = Projeto.objects.get(pk=projeto_FK.id)

    if request.POST:
        descricaoForm = request.POST['descricao']
        meioForm = request.POST['meio_FK']
        tipo_areaForm = request.POST['tipo_area_FK']
        areaForm = request.POST['area_FK']
        obj = Diagnostico.objects.get(pk=diagnostico)
        obj.descricao = descricaoForm
        obj.meio_FK_id = meioForm
        obj.tipo_area_FK_id = tipo_areaForm
        obj.area_FK_id = areaForm
        obj.save()
        return redirect('/impacto/perfil_projeto/'+str(projeto_FK.id)+"/")

    if not projeto_FK.data_termino:
        projeto_FK.data_termino = "Não Determinado"

    context['projeto'] = {'nome': projeto_FK.nome,
                          'id': projeto_FK.id,
                          'descricao': projeto_FK.descricao,
                          'codigo': projeto_FK.cod_projeto,
                          'status': projeto_FK.status_FK,
                          'data_inicio': projeto_FK.data_inicio,
                          'data_termino': projeto_FK.data_termino}

    context['cliente'] = {'nome': projeto_FK.cliente_FK.nome, 'cnpj': projeto_FK.cliente_FK.cnpj}
    context['diagnostico_id'] = diagnostico
    context['fase'] = {'nome': diagnostico_FK.fase_projeto_FK.get_descricao_display}
    context['form'] = DiagnosticoForm(instance=diagnostico_FK)

    return render(request, "impacto/edit_diagnostico.html", context)
