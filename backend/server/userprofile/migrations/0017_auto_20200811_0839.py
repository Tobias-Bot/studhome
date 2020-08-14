# Generated by Django 3.0.4 on 2020-08-11 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0016_settings_blur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='background',
            field=models.ImageField(blank=True, default='', upload_to='setting_covers/'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='unsplash_background',
            field=models.TextField(blank=True, default='', max_length=300),
        ),
    ]
