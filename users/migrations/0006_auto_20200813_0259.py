# Generated by Django 2.1.7 on 2020-08-12 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200811_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='categories',
            field=models.CharField(choices=[('Freelancer', 'Freelancer'), ('Investor', 'Investor'), ('Intern/Employee', 'Intern/Employee'), ('Co-founder', 'Co-founder'), ('Franchisee', 'Franchisee')], max_length=100),
        ),
    ]
