# Generated by Django 5.0.2 on 2024-08-03 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0051_manufacturing_harvest_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufacturing',
            name='Fuel_Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='manufacturing',
            name='Harvest_Acer_Cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='manufacturing',
            name='Total_Fuel',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='manufacturing',
            name='Total_Harvest_Acer',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='expense',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='manufacturing',
            name='Harvest_Type',
            field=models.CharField(choices=[(' WITH_FUEL', ' WITH_FUEL'), ('  WITHOUT_FUEL', '   WITHOUT_FUEL'), ('OTHERS', 'OTHERS')], default='OTHERS', max_length=20),
        ),
    ]
