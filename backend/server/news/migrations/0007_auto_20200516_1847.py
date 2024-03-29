# Generated by Django 3.0.2 on 2020-05-16 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_auto_20200506_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='document',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='image',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='news.Post'),
        ),
        migrations.AlterField(
            model_name='document',
            name='post',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='docs', to='news.Post'),
        ),
        migrations.AlterField(
            model_name='image',
            name='post',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='images', to='news.Post'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.TextField(default='', max_length=500),
        ),
    ]
