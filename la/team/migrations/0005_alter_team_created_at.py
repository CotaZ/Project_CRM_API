# Generated by Django 4.2.4 on 2023-11-21 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0004_alter_team_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
