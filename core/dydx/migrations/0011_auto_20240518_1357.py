# Generated by Django 3.2.23 on 2024-05-18 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dydx', '0010_alter_wallet_telegram_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='makepositions',
            old_name='size',
            new_name='ratio',
        ),
        migrations.AddField(
            model_name='makepositions',
            name='position_status',
            field=models.CharField(choices=[('open', 'open'), ('close', 'close')], default='open', max_length=256),
        ),
        migrations.AddField(
            model_name='positions',
            name='make_position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dydx.makepositions'),
        ),
    ]
