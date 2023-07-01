from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    phone = models.CharField(verbose_name='Телефон', max_length=20)

    def __str__(self):
        return self.username + ' ' + self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class City(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100, unique=True)
    created_tm = models.DateTimeField(verbose_name='Время создания', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']


class Building(models.Model):
    city = models.ForeignKey(City, verbose_name='Название', related_name='cities', on_delete=models.CASCADE)
    street = models.CharField(verbose_name='Улица', max_length=255)
    number = models.CharField(verbose_name='Номер', max_length=30)
    latitude = models.DecimalField(verbose_name='Широта', max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(verbose_name='Долгота', max_digits=10, decimal_places=8, blank=True, null=True)
    created_tm = models.DateTimeField(verbose_name='Время создания', auto_now=True)

    def __str__(self):
        return self.street + ' ' + self.number

    class Meta:
        verbose_name = 'Здание'
        verbose_name_plural = 'Здания'
        unique_together = ('city', 'street', 'number')


class SpaceType(models.Model):
    name = models.CharField(verbose_name='Название', max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип помещения'
        verbose_name_plural = 'Типы помещения'
        ordering = ['name']


class RentType(models.Model):
    name = models.CharField(verbose_name='Название', max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип аренды'
        verbose_name_plural = 'Типы аренды'
        ordering = ['name']


class Space(models.Model):
    building = models.ForeignKey(Building, verbose_name='Здание', related_name='buildings', on_delete=models.CASCADE)
    day_price = models.DecimalField(verbose_name='Цена за день', max_digits=10, decimal_places=2, null=True)
    month_price = models.DecimalField(verbose_name='Цена за месяц', max_digits=10, decimal_places=2, null=True)
    type = models.ForeignKey(SpaceType, verbose_name='Тип помещения', related_name='spaces', on_delete=models.CASCADE)
    rent_type = models.ForeignKey(RentType, verbose_name='Срок аренды', related_name='spaces', on_delete=models.CASCADE)
    area = models.DecimalField(verbose_name='Площадь', max_digits=10, decimal_places=2)
    rooms_number = models.IntegerField(verbose_name='Количество комнат', blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Владелец объявления', related_name='spaces', on_delete=models.CASCADE)
    created_tm = models.DateTimeField(verbose_name='Время создания', auto_now=True)
    views = models.IntegerField(verbose_name='Количество просмотров', default=0)

    def __str__(self):
        return f'Помещение {self.id}'

    class Meta:
        verbose_name = 'Помещение'
        verbose_name_plural = 'Помещения'


class SpaceImage(models.Model):
    space = models.ForeignKey(Space, verbose_name='Помещение',  default=None, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(verbose_name='Фотография', upload_to='images/')

    def __str__(self):
        return self.space.__str__()

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
