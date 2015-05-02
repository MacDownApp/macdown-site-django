# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sparkle', '0002_auto_20140701_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemprofilereport',
            name='ip_address',
            field=models.GenericIPAddressField(verbose_name='IP address'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='version',
            name='application',
            field=models.ForeignKey(related_name='versions', to='sparkle.Application', verbose_name='application'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='version',
            name='channels',
            field=models.ManyToManyField(related_name='versions', verbose_name='channels', to='sparkle.Channel'),
            preserve_default=True,
        ),
    ]
