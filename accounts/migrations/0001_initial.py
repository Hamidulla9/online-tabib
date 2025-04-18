# Generated by Django 5.0.13 on 2025-04-16 11:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ish_joyi', models.CharField(max_length=255)),
                ('nomi', models.CharField(max_length=255)),
                ('lavozimi', models.CharField(max_length=255)),
                ('ishga_kirgan_yili', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('passport', models.CharField(max_length=10, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('verification_code', models.CharField(blank=True, max_length=6, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserEducation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oqigan_joyi', models.CharField(max_length=255)),
                ('nomi', models.CharField(max_length=255)),
                ('yonalish', models.CharField(max_length=255)),
                ('diplom_raqami', models.CharField(max_length=50)),
                ('diplom_fayli', models.FileField(upload_to='diploms/')),
            ],
        ),
        migrations.CreateModel(
            name='Extra_work',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ish_joyi', models.CharField(max_length=255)),
                ('nomi', models.CharField(max_length=255)),
                ('lavozimi', models.CharField(max_length=255)),
                ('ishga_kirgan_yili', models.DateField()),
                ('experience', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experience', to='accounts.experience')),
            ],
        ),
        migrations.CreateModel(
            name='AdditionalUniversity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oqigan_joyi', models.CharField(max_length=255)),
                ('nomi', models.CharField(max_length=255)),
                ('yonalish', models.CharField(max_length=255)),
                ('diplom_raqami', models.CharField(max_length=50)),
                ('diplom_fayli', models.FileField(upload_to='diploms/')),
                ('user_education', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_universities', to='accounts.usereducation')),
            ],
        ),
    ]
