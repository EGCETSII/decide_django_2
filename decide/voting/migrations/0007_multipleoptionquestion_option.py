# Generated by Django 2.0 on 2020-12-19 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0006_remove_multipleoptionquestion_option'),
    ]

    operations = [
        migrations.AddField(
            model_name='multipleoptionquestion',
            name='option',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
    ]
