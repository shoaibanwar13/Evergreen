# Generated by Django 5.1.1 on 2024-10-11 11:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0070_loading_labour_advance_production_labour_advance'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Loading_Labour_Advance_Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Team_Leader', models.CharField(max_length=500)),
                ('Advance', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='LoadingLabourAdvance', to=settings.AUTH_USER_MODEL)),
                ('userprofile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Production_Labour_Advance_Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Team_Leader', models.CharField(max_length=500)),
                ('Advance', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ProductionLabourAdvance', to=settings.AUTH_USER_MODEL)),
                ('userprofile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business.profile')),
            ],
        ),
    ]
