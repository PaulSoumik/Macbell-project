# Generated by Django 2.1.7 on 2020-07-13 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0007_jobapplication_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='resume',
            field=models.FileField(blank=True, upload_to='resume'),
        ),
    ]