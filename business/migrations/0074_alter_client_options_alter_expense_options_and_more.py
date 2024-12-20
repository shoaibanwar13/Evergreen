# Generated by Django 5.1.1 on 2024-10-19 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0073_loading_labour_advance_payment_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name_plural': 'Daily Production Record'},
        ),
        migrations.AlterModelOptions(
            name='expense',
            options={'verbose_name_plural': 'Expenses'},
        ),
        migrations.AlterModelOptions(
            name='loading_labour',
            options={'verbose_name_plural': 'Loading Labours'},
        ),
        migrations.AlterModelOptions(
            name='loading_labour_advance_payment',
            options={'verbose_name_plural': 'Loading Labour Advance Payment'},
        ),
        migrations.AlterModelOptions(
            name='loadinglabourrecord',
            options={'verbose_name_plural': 'Loadings Labours Record'},
        ),
        migrations.AlterModelOptions(
            name='manufacturing',
            options={'verbose_name_plural': 'Manufacturing Records'},
        ),
        migrations.AlterModelOptions(
            name='paymentout',
            options={'verbose_name_plural': 'Transactions'},
        ),
        migrations.AlterModelOptions(
            name='producctionlabourrecord',
            options={'verbose_name_plural': 'Production Labours Record'},
        ),
        migrations.AlterModelOptions(
            name='production_labour',
            options={'verbose_name_plural': 'Productions Labours'},
        ),
        migrations.AlterModelOptions(
            name='production_labour_advance_payment',
            options={'verbose_name_plural': 'Production Labour Advance Payment'},
        ),
        migrations.AlterModelOptions(
            name='sale',
            options={'verbose_name_plural': 'Sales Record'},
        ),
        migrations.AlterModelOptions(
            name='sale_return',
            options={'verbose_name_plural': 'Sales Returns'},
        ),
    ]
