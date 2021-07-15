# Generated by Django 3.0.2 on 2020-06-16 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20200615_1653'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='date',
            new_name='creation_date',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='subscribers_count',
            new_name='subs',
        ),
        migrations.AddField(
            model_name='room',
            name='adminname',
            field=models.CharField(default='FirstUser', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='image',
            field=models.ImageField(blank=True, upload_to='room_covers/'),
        ),
        migrations.AlterField(
            model_name='room',
            name='description',
            field=models.CharField(default='', max_length=3000),
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
