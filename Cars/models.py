from django.db import models
from django.core.exceptions import ValidationError
class Car(models.Model):
    FUEL_CHOICES = [
        ('бензин', 'Бензин'),
        ('дизель', 'Дизель'),
        ('электричество', 'Электричество'),
        ('гибрид', 'Гибрид'),
    ]

    TRANSMISSION_CHOICES = [
        ('механическая', 'Механическая'),
        ('автоматическая', 'Автоматическая'),
        ('вариатор', 'Вариатор'),
        ('робот', 'Робот'),
    ]

    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    mileage = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.year < 1886 or self.year > 2024:
            raise ValidationError({'year': 'Год выпуска должен быть в диапазоне от 1886 до 2024.'})
        if self.mileage < 0:
            raise ValidationError({'mileage': 'Пробег не может быть отрицательным.'})
        if self.price < 0:
            raise ValidationError({'price': 'Цена не может быть отрицательной.'})
        if self.fuel_type not in dict(self.FUEL_CHOICES):
            raise ValidationError({'fuel_type': 'Неверный тип топлива.'})
        if self.transmission not in dict(self.TRANSMISSION_CHOICES):
            raise ValidationError({'transmission': 'Неверный тип трансмиссии.'})
    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"
