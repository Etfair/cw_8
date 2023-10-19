from django.core.validators import MaxValueValidator
from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


# Create your models here.
class Habit(models.Model):
    """
    Общая модель для всех привычек
     Пользователь
    Место
    Время
    Действие
    Признак приятной привычки
    Связанная привычка
    Периодичность(по умолчанию ежедневная)
    Вознаграждение
    Время на выполнение —
    Признак публичности
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE,
                              verbose_name='владелец')
    place = models.CharField(max_length=150, verbose_name='место выполения привычки')
    time = models.TimeField(verbose_name='время')
    action = models.CharField(max_length=150, verbose_name='действие')
    sign_pleasant_habit = models.BooleanField(default=False, verbose_name='Признак приятной привычки', **NULLABLE)
    related_habit = models.BooleanField(default=False, verbose_name='Связанная привычка', **NULLABLE)
    period = models.IntegerField(default=1, verbose_name='периодичность в днях',
                                 validators=[MaxValueValidator(7)], **NULLABLE)
    award = models.CharField(max_length=150, verbose_name='вознаграждение', **NULLABLE)
    time_to_complete = models.PositiveSmallIntegerField(default=60, validators=[MaxValueValidator(120)],
                                                        verbose_name='время на выполнение', **NULLABLE)
    is_published = models.BooleanField(default=False, verbose_name='признак публичности', **NULLABLE)

    def __str__(self):
        return f'{self.owner} выполняет({self.action}) - {self.time} {self.place}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
