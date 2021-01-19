# Generated by Django 2.1.7 on 2020-08-11 17:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forms', '0022_auto_20200811_2216'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('im', models.CharField(choices=[('student', 'student'), ('enterpreneur', 'enterpreneur'), ('Businessman', 'Businessman'), ('Investor', 'Investor'), ('Freelancers', 'Freelancers'), ('Student Enterpreneur', 'Student Enterpreneur')], max_length=100)),
                ('work_at', models.CharField(blank=True, max_length=100)),
                ('education', models.CharField(max_length=100)),
                ('experience', models.CharField(max_length=100)),
                ('about', models.CharField(blank=True, max_length=300)),
                ('skills', models.ManyToManyField(to='forms.SKILLS')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Employee_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InternProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('im', models.CharField(choices=[('student', 'student'), ('enterpreneur', 'enterpreneur'), ('Businessman', 'Businessman'), ('Investor', 'Investor'), ('Freelancers', 'Freelancers'), ('Student Enterpreneur', 'Student Enterpreneur')], max_length=100)),
                ('work_at', models.CharField(blank=True, max_length=100)),
                ('education', models.CharField(max_length=100)),
                ('experience', models.CharField(max_length=100)),
                ('about', models.CharField(blank=True, max_length=300)),
                ('skills', models.ManyToManyField(to='forms.SKILLS')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Intern_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InvestorProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('im', models.CharField(choices=[('student', 'student'), ('enterpreneur', 'enterpreneur'), ('Businessman', 'Businessman'), ('Investor', 'Investor'), ('Freelancers', 'Freelancers'), ('Student Enterpreneur', 'Student Enterpreneur')], max_length=100)),
                ('area_of_invest', models.CharField(max_length=100)),
                ('firm_name', models.CharField(max_length=100)),
                ('website', models.URLField()),
                ('investment_location', models.CharField(max_length=100)),
                ('investment_range', models.CharField(blank=True, max_length=20)),
                ('previous_investment', models.CharField(blank=True, max_length=20)),
                ('about', models.CharField(blank=True, max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Investor_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameField(
            model_name='companybase',
            old_name='Businesstype',
            new_name='businesstype',
        ),
        migrations.RenameField(
            model_name='companybase',
            old_name='City',
            new_name='company_address',
        ),
        migrations.RenameField(
            model_name='products',
            old_name='Description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='products',
            old_name='Prod_name',
            new_name='prod_name',
        ),
        migrations.RemoveField(
            model_name='companybase',
            name='About_cmp',
        ),
        migrations.RemoveField(
            model_name='companybase',
            name='cmp_address',
        ),
        migrations.AddField(
            model_name='companybase',
            name='about_company',
            field=models.CharField(default=0, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companybase',
            name='brand_name',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companybase',
            name='city',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='companybase',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companybase',
            name='logo',
            field=models.ImageField(blank=True, upload_to='logo_pics'),
        ),
        migrations.AddField(
            model_name='products',
            name='minimum_no',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='products',
            name='price',
            field=models.CharField(default=0, max_length=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='companybase',
            name='company_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='companybase',
            name='industry',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='companybase',
            name='website',
            field=models.URLField(),
        ),
    ]
