# Generated by Django 3.0.2 on 2020-07-13 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0007_settings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='blackout',
            field=models.SmallIntegerField(default=0),
        ),
    ]
