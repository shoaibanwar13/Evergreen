# Generated by Django 5.1.1 on 2024-10-11 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0068_remove_loading_labour_labour_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='producctionlabourrecord',
            name='Labour_Id',
            field=models.IntegerField(default=0),
        ),
    ]