# Generated by Django 4.2.4 on 2023-11-14 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0008_lead_team'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lead',
            options={'ordering': ('name',)},
        ),
    ]
