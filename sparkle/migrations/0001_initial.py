# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ghostdown.models.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='name', max_length=50)),
                ('slug', models.SlugField(verbose_name='slug', unique=True)),
            ],
            options={
                'verbose_name_plural': 'applications',
                'verbose_name': 'application',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SystemProfileReport',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('ip_address', models.IPAddressField(verbose_name='IP address')),
                ('created_at', models.DateTimeField(verbose_name='created at', auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SystemProfileReportRecord',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('key', models.CharField(verbose_name='key', max_length=100)),
                ('value', models.CharField(verbose_name='value', max_length=80)),
                ('report', models.ForeignKey(to='sparkle.SystemProfileReport', verbose_name='report')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=100)),
                ('version', models.CharField(verbose_name='version', help_text='If you use short_version, this can be the internal version number or build number that will not be shown. In any case, this string is compared to CFBundleVersion of your bundle.', max_length=10)),
                ('short_version', models.CharField(verbose_name='short version', max_length=50, help_text='A user-displayable version string.', blank=True)),
                ('dsa_signature', models.CharField(verbose_name='DSA signature', max_length=80)),
                ('length', models.CharField(verbose_name='length', max_length=20)),
                ('release_notes', ghostdown.models.fields.GhostdownField(verbose_name='release notes', blank=True)),
                ('minimum_system_version', models.CharField(verbose_name='minimum system version', max_length=10)),
                ('update_url', models.URLField(verbose_name='update URL')),
                ('created_at', models.DateTimeField(verbose_name='created at', auto_now_add=True)),
                ('publish_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='published at', help_text='When this upate will be (automatically) published.')),
                ('application', models.ForeignKey(to='sparkle.Application', verbose_name='application')),
            ],
            options={
                'verbose_name_plural': 'versions',
                'verbose_name': 'version',
                'get_latest_by': 'publish_at',
                'ordering': ('-publish_at',),
            },
            bases=(models.Model,),
        ),
    ]
