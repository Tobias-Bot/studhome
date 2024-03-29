# Generated by Django 3.0.2 on 2020-06-29 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0013_auto_20200629_1703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='video_url',
        ),
        migrations.RemoveField(
            model_name='post',
            name='images',
        ),
        migrations.AddField(
            model_name='document',
            name='cover',
            field=models.ImageField(blank=True, upload_to='doc_covers/'),
        ),
        migrations.AddField(
            model_name='image',
            name='post',
            field=models.ForeignKey(default=137, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='news.Post'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='username',
            field=models.CharField(default='FirstUser', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='video_url',
            field=models.TextField(blank=True, default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='news.Post'),
        ),
        migrations.AlterField(
            model_name='document',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.Post'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(blank=True, upload_to='post_images/'),
        ),
        migrations.AlterField(
            model_name='note',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='note', to='news.Post'),
        ),
    ]
