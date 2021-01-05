# Generated by Django 2.0 on 2021-01-05 10:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0009_merge_20210105_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voting',
            name='link',
            field=models.CharField(default='', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only letters and numbers are allowed.')]),
        ),
    ]
