# Generated by Django 4.2.7 on 2023-11-15 19:25

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0003_team_plan'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lead', '0011_leadfield'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LeadField',
            new_name='LeadFile',
        ),
    ]
