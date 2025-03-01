# Generated by Django 3.2.23 on 2024-05-18 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dydx', '0007_auto_20240404_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='historyfunding',
            name='creation_time',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='historytrades',
            name='creation_time',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='historytransfers',
            name='creation_time',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='historyfunding',
            name='funding_rate',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='historyfunding',
            name='payment',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='historyfunding',
            name='ppsition',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='historytrades',
            name='amount',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='historytrades',
            name='fee',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='historytrades',
            name='price',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='historytrades',
            name='total',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='historytransfers',
            name='amount',
            field=models.CharField(max_length=256),
        ),
    ]
