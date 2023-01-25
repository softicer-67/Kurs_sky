from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models


class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class File(models.Model):
    NEW_STATUS = 'new'
    UPDATED_STATUS = 'updated'
    VERIFIED_STATUS = 'verified'

    STATUS = (
        (NEW_STATUS, 'new'),
        (UPDATED_STATUS, 'updated'),
        (VERIFIED_STATUS, 'verified')
    )

    # name = models.CharField('Название', max_length=150)
    # slug = models.SlugField(max_length=150, null=True, blank=True, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец')
    file = models.FileField('Файл', upload_to='files/', validators=[FileExtensionValidator(['py'])])
    status = models.CharField(choices=STATUS, default=NEW_STATUS, max_length=8)
    created_at = models.DateTimeField('Время создания', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    def __str__(self):
        return self.name


class Logs(models.Model):
    file = models.ForeignKey(File, null=True, on_delete=models.CASCADE, verbose_name='Файл')
    logs = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    send_mail = models.BooleanField(default=False)
