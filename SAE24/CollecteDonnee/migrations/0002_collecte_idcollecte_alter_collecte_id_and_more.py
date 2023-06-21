# Generated by Django 4.1.7 on 2023-06-21 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CollecteDonnee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='collecte',
            name='idcollecte',
            field=models.CharField(default=0, max_length=50),
        ),
        migrations.AlterField(
            model_name='collecte',
            name='id',
            field=models.SmallAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='collecte',
            name='piece',
            field=models.CharField(max_length=255, verbose_name='Pièce'),
        ),
    ]
