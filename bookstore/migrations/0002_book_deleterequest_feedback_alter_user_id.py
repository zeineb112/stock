# Generated by Django 4.2.9 on 2024-07-29 09:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('year', models.CharField(max_length=100)),
                ('publisher', models.CharField(max_length=200)),
                ('desc', models.CharField(max_length=1000)),
                ('uploaded_by', models.CharField(blank=True, max_length=100, null=True)),
                ('user_id', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateField(default=datetime.date.today, max_length=12)),
                ('time', models.CharField(default='00:00', max_length=12)),
                ('status', models.BooleanField(default=False)),
                ('controle', models.CharField(default='', max_length=100)),
                ('time1', models.CharField(default='00:00', max_length=12)),
                ('time2', models.CharField(default='00:00', max_length=12)),
                ('is_publisher', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('urgent', models.CharField(default='', max_length=100)),
                ('Nands', models.CharField(default='', max_length=100)),
                ('conforme', models.CharField(default='', max_length=100)),
                ('type', models.CharField(default='None', max_length=100)),
                ('fiche', models.CharField(default='None', max_length=100)),
                ('implutation', models.CharField(default='None', max_length=100)),
                ('UAP', models.CharField(default='', max_length=100)),
                ('time_difference', models.CharField(default='', max_length=100)),
                ('produit', models.CharField(default='1', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DeleteRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delete_request', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
