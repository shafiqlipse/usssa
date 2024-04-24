# Generated by Django 5.0.1 on 2024-03-09 08:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Official',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('email', models.EmailField(blank=True, default='', max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, default='', max_length=15, null=True)),
                ('nin', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, null=True)),
                ('role', models.CharField(blank=True, choices=[('Referee', 'Referee'), ('Umpire', 'Umpire'), ('Moderator', 'Moderator')], max_length=10, null=True)),
                ('bio', models.TextField(blank=True)),
                ('photo', models.ImageField(blank=True, default='/images/profile.png', null=True, upload_to='photos/')),
                ('sport', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='official', to='accounts.sport')),
            ],
        ),
    ]
