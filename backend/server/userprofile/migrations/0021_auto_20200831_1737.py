# Generated by Django 3.1 on 2020-08-31 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0020_auto_20200816_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.TextField(max_length=50),
        ),
    ]