# Generated by Django 4.2.7 on 2023-12-16 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_delete_followercount_profiledatamodel_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiledatamodel',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profiledatamodel',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profiledatamodel',
            name='profileimg',
            field=models.ImageField(blank=True, default='blank-profile-picture.png', upload_to='profile_images'),
        ),
    ]