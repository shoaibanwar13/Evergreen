# Generated by Django 5.0.2 on 2024-07-31 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0048_manufacturing_manufacturing_purchase_typye'),
    ]

    operations = [
        migrations.RenameField(
            model_name='manufacturing',
            old_name='Manufacturing_Purchase_Typye',
            new_name='Manufacturing_Purchase_Type',
        ),
    ]
