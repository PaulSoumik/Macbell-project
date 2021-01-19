# Generated by Django 2.1.7 on 2020-08-06 19:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forms', '0013_auto_20200720_2144'),
    ]

    operations = [
        migrations.CreateModel(
            name='FreelancersProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('im', models.CharField(choices=[('student', 'student'), ('enterpreneur', 'enterpreneur'), ('Businessman', 'Businessman'), ('Employee', 'Employee')], max_length=100)),
                ('aualification', models.CharField(max_length=100)),
                ('workingas', models.CharField(max_length=100)),
                ('workas', models.CharField(max_length=100)),
                ('interestedin', models.CharField(max_length=200)),
                ('lookingfor', models.CharField(max_length=200)),
                ('workpay', models.IntegerField(default=0)),
                ('prevwork', models.CharField(max_length=200)),
                ('industry', models.CharField(max_length=100)),
                ('portfoliolink', models.URLField()),
                ('about', models.TextField(max_length=400)),
                ('skills', models.ManyToManyField(to='forms.SKILLS')),
                ('theuser', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='FreelancerUserProfile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
