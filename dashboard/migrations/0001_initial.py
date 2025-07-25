# Generated by Django 5.1.6 on 2025-06-27 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CoordonneesSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=255, unique=True)),
                ('type_site', models.CharField(max_length=50)),
                ('nombre_menages', models.PositiveIntegerField(default=0)),
                ('nombre_individus', models.PositiveIntegerField(default=0)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='HistoriqueSynchro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dernier_synchro', models.DateTimeField(auto_now_add=True, verbose_name='Dernier synchro')),
            ],
        ),
        migrations.CreateModel(
            name='MouvementDeplace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provenance', models.CharField(max_length=255)),
                ('menage', models.PositiveIntegerField()),
                ('individus', models.PositiveIntegerField()),
                ('personne_vivant_handicape', models.PositiveIntegerField(default=0)),
                ('typemouvement', models.CharField(max_length=50)),
                ('raison', models.CharField(max_length=255)),
                ('statutmouvement', models.CharField(max_length=50)),
                ('individu_tranche_age_0_4_f', models.PositiveBigIntegerField(default=0)),
                ('individu_tranche_age_5_11_f', models.PositiveBigIntegerField(default=0)),
                ('individu_tranche_age_12_17_f', models.PositiveBigIntegerField(default=0)),
                ('individu_tranche_age_18_24_f', models.PositiveBigIntegerField(default=0)),
                ('individu_tranche_age_25_59_f', models.PositiveBigIntegerField(default=0)),
                ('individu_tranche_age_60_f', models.PositiveBigIntegerField(default=0)),
                ('individu_tranche_age_0_4_h', models.PositiveBigIntegerField(default=0)),
                ('individu_tranche_age_5_11_h', models.PositiveBigIntegerField(default=0)),
                ('individu_tranche_age_12_17_h', models.PositiveBigIntegerField(default=0)),
                ('individu_tranche_age_18_24_h', models.PositiveBigIntegerField(default=0)),
                ('individu_tranche_age_25_59_h', models.PositiveBigIntegerField(default=0)),
                ('individu_tranche_age_60_h', models.PositiveBigIntegerField(default=0)),
                ('province', models.CharField(blank=True, max_length=50, null=True)),
                ('territoire', models.CharField(blank=True, max_length=50, null=True)),
                ('zone_sante', models.CharField(blank=True, max_length=50, null=True)),
                ('site', models.CharField(blank=True, max_length=50, null=True)),
                ('type_site', models.CharField(blank=True, max_length=50, null=True)),
                ('coordinateur_site', models.CharField(blank=True, max_length=50, null=True)),
                ('gestionnaire_site', models.CharField(blank=True, max_length=50, null=True)),
                ('sous_mecanisme', models.BooleanField(default=False)),
                ('organisation', models.CharField(blank=True, max_length=50, null=True)),
                ('activite', models.PositiveBigIntegerField(default=1)),
                ('enqueteur', models.CharField(blank=True, max_length=50, null=True)),
                ('date_enregistrement', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
