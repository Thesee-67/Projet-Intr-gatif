from django.db import models

class Collecte(models.Model):
    id = models.SmallAutoField(primary_key=True)
    idcollecte = models.CharField(max_length=50, default=0)
    piece = models.CharField(max_length=255, verbose_name='Pièce')
    date = models.DateField(verbose_name='Date')
    heure = models.TimeField(verbose_name='Heure')
    temp = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Température')

    def __str__(self):
        return self.piece
