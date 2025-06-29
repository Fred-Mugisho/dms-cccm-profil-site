# Generated by Django 5.1.6 on 2025-06-28 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coordonneessite',
            name='coordinateur_site',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='coordonneessite',
            name='gestionnaire_site',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='coordonneessite',
            name='province',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='coordonneessite',
            name='sous_mecanisme',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='coordonneessite',
            name='territoire',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='coordonneessite',
            name='zone_sante',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
