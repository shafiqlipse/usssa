# Generated by Django 5.0.1 on 2024-03-09 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('athletes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='athlete',
            name='lin',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
