# Generated by Django 3.0.2 on 2020-06-26 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_auto_20200626_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='rooms_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='blogs',
            field=models.TextField(default='мой первый блог', max_length=1500),
        ),
    ]
