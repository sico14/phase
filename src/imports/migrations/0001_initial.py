# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('documents', '0002_document_favorited_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Import',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('line', models.IntegerField(verbose_name='Line')),
                ('status', models.CharField(default='new', max_length=50, verbose_name='Status', choices=[('new', 'New'), ('success', 'Success'), ('error', 'Error')])),
                ('errors', models.TextField(null=True, verbose_name='Errors', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImportBatch',
            fields=[
                ('uid', django_extensions.db.fields.UUIDField(max_length=36, serialize=False, editable=False, primary_key=True, blank=True)),
                ('file', models.FileField(upload_to='import_%Y%m%d', verbose_name='File')),
                ('status', models.CharField(default='new', max_length=50, verbose_name='Status', choices=[('new', 'New'), ('started', 'Started'), ('success', 'Success'), ('partial_success', 'Partial success'), ('error', 'Error')])),
                ('created_on', models.DateField(default=django.utils.timezone.now, verbose_name='Created on')),
                ('category', models.ForeignKey(verbose_name='Category', to='categories.Category')),
            ],
            options={
                'ordering': ['-created_on'],
                'verbose_name': 'Import batch',
                'verbose_name_plural': 'Import batches',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='import',
            name='batch',
            field=models.ForeignKey(verbose_name='Batch', to='imports.ImportBatch'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='import',
            name='document',
            field=models.ForeignKey(blank=True, to='documents.Document', null=True),
            preserve_default=True,
        ),
    ]
