# Generated by Django 2.1.7 on 2020-08-08 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0015_auto_20200807_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategories',
            name='forcategory',
            field=models.CharField(choices=[('Business Advisor', 'Business Advisor'), ('Financial Advisor', 'Financial Advisor'), ('Technical Advisor', 'Technical Advisor'), ('Legal Advisor', 'Legal Advisor'), ('Chater Accountant', 'Chater Accountant'), ('Company secretary', 'Company secretary'), ('Content Writter', 'Content Writter'), ('Graphic Designer', 'Graphic Designer'), ('Adv. Film Maker', 'Adv. Film Maker'), ('Web Developer', 'Web Developer'), ('Software Developer', 'Software Developer'), ('App Developer', 'App Developer'), ('Digital Marketing', 'Digital Marketing'), ('Event Planner', 'Event Planner'), ('Data Entry Operator', 'Data Entry Operator'), ('Telecaller', 'Telecaller'), ('Markeitng', 'Markeitng'), ('Hr', 'Hr')], default='Legal Advisor', max_length=100),
        ),
    ]