# Generated by Django 5.0.2 on 2024-07-08 04:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0035_remove_manufacturing_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='Pending_Payments',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='Recived_Payments',
        ),
    ]
