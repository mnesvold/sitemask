# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mask',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.TextField(blank=True)),
                ('subtitle', models.TextField(blank=True)),
                ('image', models.ImageField(upload_to='')),
                ('effective', models.DateTimeField()),
                ('expiration', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='mask',
            unique_together=set([('effective', 'expiration')]),
        ),
    ]
