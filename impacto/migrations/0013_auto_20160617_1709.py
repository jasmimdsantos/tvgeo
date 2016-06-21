# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-17 20:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('impacto', '0012_auto_20160614_1647'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario_Questionario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_inclusao', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Inclusão')),
                ('nome', models.CharField(max_length=50, verbose_name='Descrição')),
                ('endereco', models.CharField(max_length=50, verbose_name='Endereço')),
                ('compl', models.CharField(max_length=10, verbose_name='Compl')),
                ('bairro', models.CharField(max_length=40, verbose_name='Bairro')),
                ('cidade', models.CharField(max_length=50, verbose_name='Cidade')),
                ('uf', models.CharField(max_length=2, verbose_name='Estado')),
                ('cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('telefone', models.CharField(max_length=9, verbose_name='Telefone')),
                ('email', models.CharField(max_length=50, verbose_name='Descrição')),
            ],
        ),
        migrations.RenameField(
            model_name='questrespitem',
            old_name='quest_comunid_resp_item_FK',
            new_name='quest_item_FK',
        ),
        migrations.RemoveField(
            model_name='questionario',
            name='fase_projeto_FK',
        ),
        migrations.AddField(
            model_name='questionario',
            name='projeto_FK',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='impacto.Projeto', verbose_name='Projeto'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='quadroitem',
            name='classe',
            field=models.TextField(blank=True, verbose_name='Classe'),
        ),
        migrations.AlterField(
            model_name='quadroitem',
            name='descricao1',
            field=models.TextField(blank=True, verbose_name='Descrição Secundária'),
        ),
        migrations.AlterField(
            model_name='quadroitem',
            name='escala',
            field=models.TextField(blank=True, verbose_name='Escala'),
        ),
        migrations.AlterField(
            model_name='questao',
            name='tipo',
            field=models.CharField(choices=[('A', 'Aberta'), ('M', 'Multipla'), ('U', 'Única')], max_length=1),
        ),
        migrations.DeleteModel(
            name='QuestResp',
        ),
        migrations.AddField(
            model_name='usuario_questionario',
            name='questionario_FK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impacto.Questionario', verbose_name='Questionario'),
        ),
        migrations.AddField(
            model_name='questrespitem',
            name='usuario',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='impacto.Usuario_Questionario', verbose_name='Usuario'),
            preserve_default=False,
        ),
    ]