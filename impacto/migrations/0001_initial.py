# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-06 16:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnostico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=50, verbose_name='Descrição')),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnpj', models.CharField(max_length=19, verbose_name='CNPJ')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='FaseProjeto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField(default='', verbose_name='Descrição da Fase')),
                ('data_inclusao', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Inclusão')),
                ('data_inicio', models.DateField(verbose_name='Início')),
                ('data_termino', models.DateField(blank=True, null=True, verbose_name='Termino')),
                ('data_encerramento', models.DateField(blank=True, null=True, verbose_name='Encerramento')),
            ],
        ),
        migrations.CreateModel(
            name='Impacto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=250, verbose_name='Nome')),
                ('conceito', models.TextField(default='', verbose_name='Descrição')),
            ],
        ),
        migrations.CreateModel(
            name='ImpactoProjeto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=50, verbose_name='Descrição')),
                ('fase_projeto_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impacto.FaseProjeto', verbose_name='Fase Projeto')),
                ('impacto_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impacto.Impacto', verbose_name='Impacto')),
            ],
        ),
        migrations.CreateModel(
            name='Meio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=50, verbose_name='Descrição')),
            ],
        ),
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projeto_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impacto.Empresa', verbose_name='Projeto')),
                ('usuario', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('cod_projeto', models.CharField(max_length=100, unique=True, verbose_name='Código Projeto')),
                ('descricao', models.TextField(default='', verbose_name='Descição')),
                ('data_inclusao', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Inclusão')),
                ('data_inicio', models.DateField(verbose_name='Início')),
                ('data_termino', models.DateField(blank=True, null=True, verbose_name='Termino')),
                ('data_encerramento', models.DateField(blank=True, null=True, verbose_name='Encerramento')),
                ('cliente_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impacto.Empresa', verbose_name='Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Quadro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordem', models.IntegerField(verbose_name='Ordem')),
                ('descricao', models.TextField(verbose_name='Descrição')),
            ],
            options={
                'ordering': ['ordem'],
            },
        ),
        migrations.CreateModel(
            name='QuadroItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classe', models.TextField(verbose_name='Classe')),
                ('descricao', models.TextField(verbose_name='Descrição')),
                ('descricao1', models.TextField(verbose_name='Descrição Secundária')),
                ('escala', models.TextField(verbose_name='Escala')),
                ('quadro_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impacto.Quadro', verbose_name='Quadro')),
            ],
        ),
        migrations.CreateModel(
            name='Questao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=50, verbose_name='Descrição')),
                ('tipo', models.CharField(choices=[('A', 'Aberta'), ('F', 'Fechada')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='QuestaoItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=50, verbose_name='Descrição')),
                ('questao_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impacto.Questao', verbose_name='Questao')),
            ],
        ),
        migrations.CreateModel(
            name='Questionario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=50, verbose_name='Descrição')),
                ('data_inclusao', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Inclusão')),
                ('data_inicio', models.DateField(verbose_name='Início')),
                ('data_termino', models.DateField(blank=True, null=True, verbose_name='Termino')),
                ('fase_projeto_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impacto.FaseProjeto', verbose_name='Fase Projeto')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionarioInterno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('impacto_projeto_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impacto.ImpactoProjeto', verbose_name='Impacto')),
                ('pessoa_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impacto.Pessoa', verbose_name='Pessoa')),
                ('quadro_item_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impacto.QuadroItem', verbose_name='Resposta')),
            ],
        ),
        migrations.CreateModel(
            name='QuestResp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_inclusao', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Inclusão')),
                ('nome', models.CharField(max_length=50, verbose_name='Descrição')),
                ('email', models.CharField(max_length=50, verbose_name='Descrição')),
                ('questionario_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impacto.Questionario', verbose_name='Questionario')),
            ],
        ),
        migrations.CreateModel(
            name='QuestRespItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=50, verbose_name='Descrição')),
                ('quest_comunid_resp_item_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impacto.QuestaoItem', verbose_name='Resposta')),
            ],
        ),
        migrations.CreateModel(
            name='Status_Projeto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=50, verbose_name='Descrição')),
            ],
        ),
        migrations.CreateModel(
            name='TipoArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=50, verbose_name='Descrição')),
            ],
        ),
        migrations.AddField(
            model_name='questao',
            name='questionario_FK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impacto.Questionario', verbose_name='Questionario'),
        ),
        migrations.AddField(
            model_name='projeto',
            name='status_FK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impacto.Status_Projeto', verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='impactoprojeto',
            name='meio_FK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impacto.Meio', verbose_name='Meio'),
        ),
        migrations.AddField(
            model_name='impactoprojeto',
            name='tipo_area_FK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impacto.TipoArea', verbose_name='Tipo Área'),
        ),
        migrations.AddField(
            model_name='impacto',
            name='meio_FK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impacto.Meio', verbose_name='Meio'),
        ),
        migrations.AddField(
            model_name='faseprojeto',
            name='projeto_FK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impacto.Projeto', verbose_name='Projeto'),
        ),
        migrations.AddField(
            model_name='faseprojeto',
            name='status_FK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impacto.Status_Projeto', verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='diagnostico',
            name='fase_projeto_FK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impacto.FaseProjeto', verbose_name='Fase Projeto'),
        ),
        migrations.AddField(
            model_name='diagnostico',
            name='meio_FK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impacto.Meio', verbose_name='Meio'),
        ),
        migrations.AddField(
            model_name='diagnostico',
            name='tipo_area_FK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impacto.TipoArea', verbose_name='Tipo Área'),
        ),
    ]
