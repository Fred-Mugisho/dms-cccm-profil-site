# Generated by Django 5.1.6 on 2025-07-05 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_coordonneessite_coordinateur_site_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='coordonneessite',
            name='url_map',
            field=models.URLField(blank=True, null=True),
        ),
    ]
