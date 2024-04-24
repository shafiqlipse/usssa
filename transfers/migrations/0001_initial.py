# Generated by Django 5.0.1 on 2024-03-16 14:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('athletes', '0002_alter_athlete_lin'),
        ('school', '0002_remove_school_official_user_school_official_school_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransferRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initiation_date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', max_length=10)),
                ('athlete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='athletes.athlete', verbose_name='')),
                ('sfrom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_school', to='school.school', verbose_name='')),
                ('sto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_school', to='school.school', verbose_name='')),
            ],
        ),
    ]