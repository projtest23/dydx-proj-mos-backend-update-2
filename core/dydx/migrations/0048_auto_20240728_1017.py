# Generated by Django 3.2.25 on 2024-07-28 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dydx', '0047_alter_closed_positions_telegram_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='closed_positions',
            name='telegram_user',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='positions',
            name='telegram_user',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='staking',
            name='telegram_user',
            field=models.CharField(default='', max_length=500),
        ),
    ]
