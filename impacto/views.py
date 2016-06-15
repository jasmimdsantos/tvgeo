from django.shortcuts import render, redirect
from .models import Quadro, \
    QuadroItem, \
    Empresa, \
    Projeto,\
    FaseProjeto, \
    ImpactoProjeto, \
    QuestionarioInterno, \
    Diagnostico, \
    Programa, \
    ProgramaImpacto, \
    Area, \
    Impacto,\
    Pessoa

from .forms import QuadroForm, Empresa_ProjetosForm, AreaForm, ImpactoProjetoForm , DiagnosticoForm
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext , loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from toolbox import sitetools
import json
from django.core.serializers.json import DjangoJSONEncoder

@csrf_exempt
def api_get_impacto(request, meio):
    context = {'impactos':[]}
    impactos_FK = Impacto.objects.filter(meio_FK_id=meio)

    for impacto in impactos_FK:
        mont = {'nome': impacto.descricao, 'id': impacto.id}
        context['impactos'].append(mont)

    return JsonResponse(context)
@login_required
def quadro(request, impacto):
    context = {}
    context['page'] = 'Quadro Questões'
    questoes = []

    quadro_FK = Quadro.objects.all()

    for quadro in quadro_FK:
        quest = {'titulo': quadro.descricao,
                 'id': quadro.id,
                 'respostas': []}

        respostas = []
        quadro_item_FK = QuadroItem.objects.filter(quadro_FK=quadro)
        for item in quadro_item_FK:
            resposta = {'msg': item.descricao,
                        'msg2':item.descricao1,
                        'id': item.id,
                        'classe': item.classe,
                        'escala': item.escala}
            respostas.append(resposta)

        quest['respostas'] = respostas
        questoes.append(quest)

    context['questoes'] = questoes
    context['impacto'] = impacto

    return render(request, 'impacto/quadro.html', context)

def respostas_gab(impacto):
    context = {}
    questionarios = QuestionarioInterno.objects.filter(impacto_projeto_FK_id=impacto).order_by('id')
    context['respostas'] = []
    context['impacto'] = impacto
    for i, quest in enumerate(questionarios):
        if i == 6:
            quest.resp_potencial.classe = quest.resp_potencial.descricao
            quest.resp_provavel.classe = quest.resp_provavel.descricao

        mont = {'potencial': quest.resp_potencial.classe,
                'provavel': quest.resp_provavel.classe,
                'criterio': quest.resp_potencial.quadro_FK.descricao_curta}

        context['respostas'].append(mont)

    return context

@csrf_exempt
@login_required
def quadro_gab(request, impacto):
    context = {'rec': True, 'programas': []}
    programas_FK = Programa.objects.all()
    for programa in programas_FK:
        mont = {'descricao': programa.descricao, 'id': programa.id}
        context['programas'].append(mont)

    context.update(respostas_gab(impacto))
    return render(request, 'impacto/quadro_gab.html', context)

@csrf_exempt
@login_required
def quadro_post(request):
    if request.method == "POST":
        if 'respGab' in request.POST:
            resp_gabarito = request.POST.getlist('respGab')
            impacto_gab = request.POST['impacto']
            string_respGab = request.POST['respGabText']

            programa_inpacto_FK = ProgramaImpacto.objects.filter(impacto_projeto_FK_id=impacto_gab)
            if programa_inpacto_FK:
                programa_inpacto_FK.delete()

            for prog in resp_gabarito:
                qry1 = ProgramaImpacto(impacto_projeto_FK_id=impacto_gab,
                                       pessoa_FK_id=request.user.id,
                                       programa_FK_id=prog)
                qry1.save()

            qry = ImpactoProjeto.objects.get(pk=impacto_gab)
            qry.aia = string_respGab
            qry.save()
            return redirect("/impacto/projetos/perfil_projeto/editar_impacto_projeto/"+impacto_gab+"/")

        else:
            json_receive = json.loads(request.body.decode("utf-8"))
            impacto = json_receive['impacto']
            user = Pessoa.objects.get(usuario_id=request.user.id).id
            respostas = json_receive['respostas']

            questionarios = QuestionarioInterno.objects.filter(impacto_projeto_FK_id=impacto)
            if questionarios:
                questionarios.delete()

            for resposta in respostas:
                qry = QuestionarioInterno(pessoa_FK_id=user,
                                          impacto_projeto_FK_id=impacto,
                                          resp_potencial_id=resposta['potencial'],
                                          resp_provavel_id=resposta['provavel'])
                qry.save()

            return HttpResponse(status=201)
    else:
        return HttpResponse(status=403)


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
        form = AreaForm(request.POST)
        if form.is_valid():
            descricao = request.POST['descricao']
            obj = Area(descricao=descricao, projeto_FK_id=projeto)
            obj.save()
            return redirect('/impacto/projetos/perfil_projeto/'+projeto+"/")
    else:
        form = AreaForm()

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

    context['form'] = form

    return render(request, "impacto/create_area.html", context)


@login_required
def create_impacto(request, projeto, faseprojeto):
    context = RequestContext(request)
    page = sitetools.sitemap ( request.get_full_path ( ) ).context
    context.update ( page )

    if request.POST:
        form = ImpactoProjetoForm(request.POST)
        if form.is_valid():
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
            return redirect('/impacto/projetos/perfil_projeto/'+projeto+"/")

    else:
        form = ImpactoProjetoForm()

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
        form = DiagnosticoForm(request.POST)
        if form.is_valid():
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
            return redirect('/impacto/projetos/perfil_projeto/'+projeto+"/")
    else:
        form = DiagnosticoForm()

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

    context['form'] = form
    context['faseprojeto'] = faseprojeto
    return render(request, "impacto/create_diagnostico.html", context)


@login_required
def perfil_projeto(request, projeto):
    context = RequestContext(request)
    page = sitetools.sitemap ( request.get_full_path ( ) ).context
    context.update(page)
    print(context)
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
        form =AreaForm(request.POST)
        if form.is_valid():
            descricao = request.POST['descricao']
            obj = Area.objects.get(pk=area)
            obj.descricao = descricao
            obj.save()
            return redirect('/impacto/projetos/perfil_projeto/'+str(area_FK.projeto_FK_id)+"/")
    else:
        form = AreaForm(instance=area_FK)

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
    context['form'] = form

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
        form = ImpactoProjetoForm(request.POST)
        if form.is_valid():
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
            return redirect('/impacto/projetos/perfil_projeto/'+str(projeto_FK.id)+"/")
    else:
        form = ImpactoProjetoForm(instance=impactoProj_FK)
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
    context['form'] = form
    context['aia'] = {'aia_gab': impactoProj_FK.aia}

    programa_json = {'programas_gab': []}
    programas_Resp = ProgramaImpacto.objects.filter(impacto_projeto_FK_id=impacto)
    for programa in programas_Resp:
        programa_json['programas_gab'].append(programa.programa_FK.descricao)

    context['aia'].update(respostas_gab(impacto))
    context['aia'].update(programa_json)
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
        form = DiagnosticoForm(request.POST)
        if form.is_valid():
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
            return redirect('/impacto/projetos/perfil_projeto/'+str(projeto_FK.id)+"/")
    else:
        form = DiagnosticoForm(instance=diagnostico_FK)

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
    context['form'] = form

    return render(request, "impacto/edit_diagnostico.html", context)
