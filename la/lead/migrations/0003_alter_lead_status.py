# Generated by Django 4.2.7 on 2023-11-10 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0002_rename_create_by_lead_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='status',
            field=models.CharField(choices=[('new', 'New'), ('contacted', 'Contacted'), ('won', 'Won'), ('lost', 'Lost')], default='new', max_length=10),
        ),
    ]
