from django.db import models

class Collecte(models.Model):
    id = models.IntegerField(primary_key=True)
    piece = models.CharField(max_length=100, verbose_name='Pièce')
    date = models.DateField(verbose_name='Date')
    heure = models.TimeField(verbose_name='Heure')
    temp = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Température')

    def __str__(self):
        return self.titre
