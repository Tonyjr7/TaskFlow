# Generated by Django 5.1.4 on 2024-12-18 22:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_account_first_name_account_last_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='account',
            name='last_name',
        ),
    ]