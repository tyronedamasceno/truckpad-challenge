from django.db import models
from django.utils import timezone

from api.enum import Gender, CnhType, VehicleType


class Location(models.Model):
    name = models.CharField('Nome da localidade', max_length=255)
    latitude = models.DecimalField(
        'Latitude', max_digits=10, decimal_places=7
    )
    longitude = models.DecimalField(
        'Longitude', max_digits=10, decimal_places=7
    )

    class Meta:
        unique_together = ['latitude', 'longitude']
        verbose_name = 'Localidade'
        verbose_name_plural = 'Localidades'

    def __str__(self):
        return self.name


class Driver(models.Model):
    name = models.CharField('Nome do motorista', max_length=255)
    birth_date = models.DateField('Data de nascimento')
    gender = models.CharField('Sexo', max_length=10, choices=Gender.choices())
    cnh_type = models.CharField(
        'Categoria da CNH', max_length=2, choices=CnhType.choices()
    )
    owns_vehicle = models.BooleanField('Possui veículo', default=False)
    is_loaded = models.BooleanField('Está carregado', default=False)
    vehicle_type = models.IntegerField(
        'Tipo do caminhão', choices=VehicleType.choices()
    )
    origin = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='drivers_origin',
    )
    destiny = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='drivers_destiny',
    )
    created_at = models.DateTimeField('Data de registro')

    class Meta:
        verbose_name = 'Motorista'
        verbose_name_plural = 'Motoristas'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super(Driver, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
