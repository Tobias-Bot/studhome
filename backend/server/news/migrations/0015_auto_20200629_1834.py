# Generated by Django 3.0.2 on 2020-06-29 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0014_auto_20200629_1743'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='title',
        ),
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
    ]
