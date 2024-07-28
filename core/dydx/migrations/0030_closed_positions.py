# Generated by Django 3.2.23 on 2024-05-25 16:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dydx', '0029_auto_20240525_0957'),
    ]

    operations = [
        migrations.CreateModel(
            name='Closed_Positions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_user', models.CharField(default='', max_length=500)),
                ('market', models.CharField(default='ETH-USD', max_length=255)),
                ('long', models.BooleanField(default=True)),
                ('size', models.FloatField()),
                ('leverage', models.FloatField()),
                ('realized_PL', models.FloatField()),
                ('average_open', models.FloatField()),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('profit', models.FloatField()),
                ('make_position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dydx.makepositions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('wallet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dydx.wallet')),
            ],
        ),
    ]
