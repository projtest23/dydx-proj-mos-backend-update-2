# Generated by Django 3.2.23 on 2024-05-24 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dydx', '0025_deposit_created_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deposit',
            name='created_date',
        ),
    ]
