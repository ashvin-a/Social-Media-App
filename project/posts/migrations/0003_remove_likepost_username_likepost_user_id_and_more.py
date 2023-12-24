# Generated by Django 4.2.7 on 2023-12-15 15:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0002_likepost_postmodel_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likepost',
            name='username',
        ),
        migrations.AddField(
            model_name='likepost',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='likepost',
            name='post_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.postmodel'),
        ),
    ]