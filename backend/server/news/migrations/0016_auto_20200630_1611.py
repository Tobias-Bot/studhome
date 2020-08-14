# Generated by Django 3.0.2 on 2020-06-30 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0015_auto_20200629_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='blog_name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='post',
            name='note_color',
            field=models.CharField(default='white', max_length=7),
        ),
        migrations.AddField(
            model_name='post',
            name='text',
            field=models.TextField(default='', max_length=10000),
        ),
        migrations.AddField(
            model_name='post',
            name='text_color',
            field=models.CharField(default='#212121', max_length=7),
        ),
        migrations.DeleteModel(
            name='Note',
        ),
    ]
