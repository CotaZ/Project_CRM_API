# Generated by Django 4.2.4 on 2023-11-20 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0003_team_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='team.plan'),
        ),
    ]
