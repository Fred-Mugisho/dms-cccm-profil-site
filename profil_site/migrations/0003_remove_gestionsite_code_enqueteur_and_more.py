# Generated by Django 5.1.6 on 2025-05-18 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profil_site', '0002_rename_informationgenerale_informationgeneraleprofilsite_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gestionsite',
            name='code_enqueteur',
        ),
        migrations.RemoveField(
            model_name='santesite',
            name='code_enqueteur',
        ),
        migrations.RemoveField(
            model_name='washsite',
            name='code_enqueteur',
        ),
        migrations.AlterField(
            model_name='santesite',
            name='enfants_non_vaccines',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
