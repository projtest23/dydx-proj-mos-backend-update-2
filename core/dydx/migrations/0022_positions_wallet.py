# Generated by Django 3.2.23 on 2024-05-22 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dydx', '0021_alter_staking_staking_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='positions',
            name='wallet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dydx.wallet'),
        ),
    ]
