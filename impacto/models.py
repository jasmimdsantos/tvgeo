from django.db import models
from django.utils import timezone
from django.conf import settings

class Status_Projeto(models.Model):
    """ tabela de status do projeto """
    descricao = models.CharField(max_length=50, verbose_name=u'Descrição')

    def __str__(self):
        return self.descricao


class Meio(models.Model):
    """ tabela de status meios """
    descricao = models.CharField(max_length=50, verbose_name=u'Descrição')

    def __str__(self):
        return self.descricao


class TipoArea(models.Model):
    """ tabela de status meios """
    descricao = models.CharField(max_length=50, verbose_name=u'Descrição')

    def __str__(self):
        return self.descricao


class Impacto(models.Model):
    """ tabela de status meios """
    meio_FK = models.ForeignKey(Meio, verbose_name='Meio')
    descricao = models.CharField(max_length=250, verbose_name=u'Nome')
    conceito = models.TextField(verbose_name='Descrição', default='')

    def __str__(self):
        return self.descricao


class Quadro(models.Model):
    ordem = models.IntegerField(verbose_name='Ordem')
    descricao = models.TextField(verbose_name=u'Descrição')

    class Meta:
        ordering = ['ordem', ]

    def __str__(self):
        return self.descricao


class QuadroItem(models.Model):
    quadro_FK = models.ForeignKey(Quadro, verbose_name='Quadro')
    classe    = models.TextField(verbose_name=u'Classe')
    descricao = models.TextField(verbose_name=u'Descrição')
    descricao1 = models.TextField(verbose_name=u'Descrição Secundária')
    escala = models.TextField(verbose_name=u'Escala')

    def __str__(self):
        return self.descricao


class Empresa(models.Model):
    """ tabela de empresas """
    cnpj = models.CharField(max_length=19, verbose_name=u'CNPJ')
    nome = models.CharField(max_length=100, verbose_name=u'Nome')

    class Meta:
        ordering = ['nome', ]

    def __str__(self):
            return self.nome


class Pessoa(models.Model):
    """ tabela de parcelas """
    projeto_FK = models.ForeignKey(Empresa, verbose_name="Projeto" )
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,  verbose_name='Usuario', default=None)

    def __str__(self):
            return str(self.usuario)


class Projeto(models.Model):
    """ tabela de projetos """
    nome = models.CharField(max_length=100, verbose_name=u'Nome')
    cliente_FK = models.ForeignKey(Empresa, verbose_name='Cliente')
    cod_projeto = models.CharField(max_length=100, unique=True, verbose_name='Código Projeto')
    descricao = models.TextField(verbose_name=u'Descição', default='')
    status_FK = models.ForeignKey(Status_Projeto, verbose_name="Status")
    data_inclusao = models.DateTimeField(default=timezone.now, verbose_name=u'Inclusão', editable=False)
    data_inicio = models.DateField(verbose_name=u'Início')
    data_termino = models.DateField(verbose_name='Termino', null=True, blank=True)
    data_encerramento = models.DateField(verbose_name='Encerramento',   null=True, blank=True)

    def __str__(self):
        return self.descricao


class FaseProjeto(models.Model):
    """ tabela de projetos """
    projeto_FK = models.ForeignKey(Projeto, verbose_name='Projeto')
    descricao = models.TextField(verbose_name=u'Descrição da Fase', default='')
    status_FK = models.ForeignKey(Status_Projeto, verbose_name="Status")
    data_inclusao = models.DateTimeField(default=timezone.now, verbose_name=u'Inclusão', editable=False)
    data_inicio = models.DateField(verbose_name=u'Início')
    data_termino = models.DateField(verbose_name='Termino', null=True, blank=True)
    data_encerramento = models.DateField(verbose_name='Encerramento', null=True, blank=True)

    def __str__(self):
        return self.descricao


class ImpactoProjeto(models.Model):
    """ tabela de status meios """
    fase_projeto_FK = models.ForeignKey(FaseProjeto, verbose_name='Fase Projeto')
    impacto_FK = models.ForeignKey(Impacto, verbose_name="Impacto")
    tipo_area_FK = models.ForeignKey(TipoArea, verbose_name='Tipo Área')
    meio_FK = models.ForeignKey(Meio, verbose_name='Meio')
    descricao = models.CharField(max_length=50, verbose_name=u'Descrição')

    def __str__(self):
        return self.descricao


class Diagnostico(models.Model):
    fase_projeto_FK = models.ForeignKey(FaseProjeto, verbose_name='Fase Projeto')
    tipo_area_FK = models.ForeignKey(TipoArea, verbose_name='Tipo Área')
    meio_FK = models.ForeignKey(Meio, verbose_name='Meio')
    descricao = models.CharField(max_length=50, verbose_name=u'Descrição')

    def __str__(self):
        return self.descricao


class QuestionarioInterno(models.Model):
    impacto_projeto_FK = models.ForeignKey(ImpactoProjeto, verbose_name='Impacto')
    pessoa_FK = models.ForeignKey(Pessoa, verbose_name="Pessoa")
    quadro_item_FK = models.ForeignKey(QuadroItem, verbose_name='Resposta')

    def __str__(self):
        return "---"


class Questionario(models.Model):
    fase_projeto_FK = models.ForeignKey(FaseProjeto, verbose_name='Fase Projeto')
    descricao = models.CharField(max_length=50, verbose_name=u'Descrição')
    data_inclusao = models.DateTimeField(default=timezone.now, verbose_name=u'Inclusão', editable=False)
    data_inicio = models.DateField(verbose_name=u'Início')
    data_termino = models.DateField(verbose_name='Termino', null=True, blank=True)

    def __str__(self):
        return self.descricao


class Questao(models.Model):

    TIPO_QUESTAO = (('A', 'Aberta'), ('F', 'Fechada'),)

    questionario_FK = models.ForeignKey(Questionario, verbose_name='Questionario')
    descricao = models.CharField(max_length=50, verbose_name=u'Descrição')
    tipo = models.CharField(max_length=1, choices=TIPO_QUESTAO)

    def __str__(self):
        return self.descricao


class QuestaoItem(models.Model):
    questao_FK = models.ForeignKey(Questao, verbose_name='Questao')
    descricao = models.CharField(max_length=50, verbose_name=u'Descrição')

    def __str__(self):
        return self.descricao


class QuestResp(models.Model):
    questionario_FK = models.ForeignKey(Questionario, verbose_name='Questionario')
    data_inclusao = models.DateTimeField(default=timezone.now, verbose_name=u'Inclusão', editable=False)
    nome = models.CharField(max_length=50, verbose_name=u'Descrição')
    email = models.CharField(max_length=50, verbose_name=u'Descrição')

    def __str__(self):
        return self.descricao


class QuestRespItem(models.Model):
    quest_comunid_resp_item_FK = models.ForeignKey(QuestaoItem, verbose_name='Resposta')
    descricao = models.CharField(max_length=50, verbose_name=u'Descrição')

    def __str__(self):
        return self.descricao



