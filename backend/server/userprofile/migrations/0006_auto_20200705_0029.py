# Generated by Django 3.0.2 on 2020-07-04 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0005_auto_20200704_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bookmarks',
            field=models.TextField(default='|', max_length=5000),
        ),
        migrations.AlterField(
            model_name='profile',
            name='subs_profiles',
            field=models.TextField(default='|', max_length=10000),
        ),
    ]
