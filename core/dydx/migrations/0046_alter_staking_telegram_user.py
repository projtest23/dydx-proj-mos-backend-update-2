# Generated by Django 3.2.25 on 2024-07-28 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dydx', '0045_auto_20240728_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staking',
            name='telegram_user',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
