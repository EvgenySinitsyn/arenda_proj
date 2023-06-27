from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.username + ' ' + self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class City(models.Model):
    name = models.CharField(max_length=100)
    created_tm = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']


class Building(models.Model):
    city = models.ForeignKey(City, related_name='cities', on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=30)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    created_tm = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.street + ' ' + self.number

    class Meta:
        verbose_name = 'Здание'
        verbose_name_plural = 'Здания'


class SpaceType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип помещения'
        verbose_name_plural = 'Типы помещения'
        ordering = ['name']


class RentType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Space(models.Model):
    building = models.ForeignKey(Building, related_name='buildings', on_delete=models.CASCADE)
    day_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    month_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    type = models.ForeignKey(SpaceType, related_name='spaces', on_delete=models.CASCADE)
    rent_type = models.ForeignKey(RentType, related_name='spaces', on_delete=models.CASCADE)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    rooms_number = models.IntegerField(blank=True, null=True)
    poster = models.ImageField(blank=True, upload_to='posters/')
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='spaces', on_delete=models.CASCADE)
    created_tm = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return f'помещение {self.id}'


class SpaceImage(models.Model):
    space = models.ForeignKey(Space, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.space.__str__()

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
