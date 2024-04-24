# Generated by Django 5.0.1 on 2024-04-15 08:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('athletes', '0003_remove_team_name'),
        ('school', '0002_remove_school_official_user_school_official_school_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schools', to='school.school'),
        ),
    ]
