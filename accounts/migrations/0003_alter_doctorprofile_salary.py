# Generated by Django 5.0.13 on 2025-04-04 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_doctorprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorprofile',
            name='salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
