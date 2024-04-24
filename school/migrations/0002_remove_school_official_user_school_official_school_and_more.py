# Generated by Django 5.0.1 on 2024-03-10 07:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school_official',
            name='user',
        ),
        migrations.AddField(
            model_name='school_official',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='school.school'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='school_official',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10),
        ),
        migrations.AlterField(
            model_name='school_official',
            name='role',
            field=models.CharField(choices=[('Coach', 'Coach'), ('Teacher', 'Teacher'), ('Games Teacher', 'Games Teacher'), ('Assistant Games Teacher', 'Assistant Games Teacher'), ('Assistant Head Teacher', 'Assistant Head Teacher'), ('Nurse', 'Nurse'), ('Doctor', 'Doctor'), ('District Education Officer', 'District Education Officer'), ('District Sports Officer', 'District Sports Officer')], max_length=55),
        ),
    ]