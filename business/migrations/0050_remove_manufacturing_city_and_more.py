# Generated by Django 5.0.2 on 2024-07-31 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0049_rename_manufacturing_purchase_typye_manufacturing_manufacturing_purchase_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manufacturing',
            name='City',
        ),
        migrations.AddField(
            model_name='manufacturing',
            name='Per_Acer_Purchase_Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100),
        ),
        migrations.AddField(
            model_name='manufacturing',
            name='Purchase_Weight_Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100),
        ),
        migrations.AddField(
            model_name='manufacturing',
            name='Total_Acers',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100),
        ),
        migrations.AlterField(
            model_name='manufacturing',
            name='Unit',
            field=models.CharField(choices=[('NONE', 'NONE'), ('KG', 'KG'), ('MUN', ' MUN'), ('OTHERS', 'OTHERS')], default='NONE', max_length=20),
        ),
    ]
