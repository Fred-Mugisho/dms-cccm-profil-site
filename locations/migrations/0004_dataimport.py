# Generated by Django 5.1.6 on 2025-06-13 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_remove_zonesante_province_zonesante_territoire'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataImport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_site', models.CharField(blank=True, max_length=300, null=True)),
                ('nom_site', models.CharField(max_length=300)),
                ('menages', models.PositiveBigIntegerField(default=0)),
                ('individus', models.PositiveBigIntegerField(default=0)),
                ('individus_0_4_f', models.PositiveBigIntegerField(default=0)),
                ('individus_5_11_f', models.PositiveBigIntegerField(default=0)),
                ('individus_12_17_f', models.PositiveBigIntegerField(default=0)),
                ('individus_18_24_f', models.PositiveBigIntegerField(default=0)),
                ('individus_25_59_f', models.PositiveBigIntegerField(default=0)),
                ('individus_60_f', models.PositiveBigIntegerField(default=0)),
                ('individus_0_4_h', models.PositiveBigIntegerField(default=0)),
                ('individus_5_11_h', models.PositiveBigIntegerField(default=0)),
                ('individus_12_17_h', models.PositiveBigIntegerField(default=0)),
                ('individus_18_24_h', models.PositiveBigIntegerField(default=0)),
                ('individus_25_59_h', models.PositiveBigIntegerField(default=0)),
                ('individus_60_h', models.PositiveBigIntegerField(default=0)),
                ('date_mise_a_jour', models.DateField()),
            ],
        ),
    ]
