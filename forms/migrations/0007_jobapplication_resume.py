# Generated by Django 2.1.7 on 2020-07-13 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0006_jobapplication_workprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='resume',
            field=models.FileField(default=1, upload_to='profile_pics'),
            preserve_default=False,
        ),
    ]