# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sparkle', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='name', max_length=50)),
                ('slug', models.SlugField(verbose_name='slug', unique=True)),
            ],
            options={
                'verbose_name': 'channel',
                'verbose_name_plural': 'channels',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='version',
            options={'ordering': ('-publish_at',), 'verbose_name': 'version', 'verbose_name_plural': 'versions', 'get_latest_by': 'version'},
        ),
        migrations.AddField(
            model_name='application',
            name='default_channel',
            field=models.ForeignKey(null=True, verbose_name='default channel', to='sparkle.Channel'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='version',
            name='channels',
            field=models.ManyToManyField(verbose_name='channels', to='sparkle.Channel'),
            preserve_default=True,
        ),
    ]
