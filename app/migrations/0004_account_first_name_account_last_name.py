# Generated by Django 5.1.4 on 2024-12-18 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_account_first_name_remove_account_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='first_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='account',
            name='last_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]