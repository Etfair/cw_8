import json
from django.utils import timezone
from celery import shared_task
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import requests
from config.settings import TELEGRAM_TOKEN
from habit.models import Habit


@shared_task
def send_message_telegram(user, message) -> None:
    """ Отправляет сообщение в Телеграм """
    token = TELEGRAM_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={user}&text={message}"
    print(user)
    response = requests.get(url)
    print(response.json())


@shared_task
def create_periodic_task(habit_pk: int):
    """При создании новой привычки создает отложенную задачу для отправки сообщения в ТГ"""

    habit = Habit.objects.filter(pk=habit_pk).first()
    user = habit.owner.chat_id
    message = f'{habit.time} наступило время выполнить {habit.action} не меньше {habit.time_to_complete} секунд.'
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=habit.period,
        period=IntervalSchedule.DAYS
    )

    PeriodicTask.objects.create(
        interval=schedule,
        name=habit.action,
        start_time=timezone.now(),
        task='habit.tasks.send_message_telegram',
        args=json.dumps([user, message])

    )
    print(message)
