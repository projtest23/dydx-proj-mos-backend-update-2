# Generated by Django 3.2.23 on 2024-05-27 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dydx', '0036_alter_staking_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegram_channel',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
