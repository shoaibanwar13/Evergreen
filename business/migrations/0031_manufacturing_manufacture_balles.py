# Generated by Django 5.0.2 on 2024-07-05 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0030_rename_date_incurred_expense_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufacturing',
            name='Manufacture_Balles',
            field=models.IntegerField(default=0),
        ),
    ]
