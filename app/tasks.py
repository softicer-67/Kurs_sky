import datetime
import subprocess
from celery import shared_task
from django.core.mail import send_mail

from .models import File, Logs


@shared_task
def verify_file():
    files = File.objects.filter(status__in=['new', 'updated'])
    for file in files:
        log_text = subprocess.run(['flake8', file.file.path], stdout=subprocess.PIPE).stdout.decode('utf-8')
        try:
            log = Logs.objects.get(file=file)
            log.logs = log_text
            log.save()
        except:
            Logs.objects.create(file=file, logs=log_text)

        file.status = File.VERIFIED_STATUS
        file.save()

        send_log_email.delay(file.id)


@shared_task
def send_log_email(pk):
    log = Logs.objects.get(pk=pk)
    log.send_mail = 1
    log.save()

    send_mail(
        'Проверка файла',
        'Проверка файла произведена.\n Результаты проверки:\n'
        f'{log.logs}',
        'skytest2023@yandex.ru',
        [log.file.owner.email]
    )
