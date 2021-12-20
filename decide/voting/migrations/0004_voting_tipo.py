# Generated by Django 2.0 on 2021-12-20 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0003_auto_20180605_0842'),
    ]

    operations = [
        migrations.AddField(
            model_name='voting',
            name='tipo',
            field=models.CharField(choices=[('IDENTITY', 'IDENTITY'), ('BIPARTITANSHIP', 'BIPARTITANSHIP')], default='IDENTITY', max_length=20, verbose_name='Count method'),
        ),
    ]
