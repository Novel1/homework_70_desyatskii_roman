from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Project(models.Model):
    name = models.CharField(max_length=60, verbose_name='Проект')
    description = models.TextField(max_length=3000, verbose_name='Описание')
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=True, null=True)
    user = models.ManyToManyField(to=User, blank=True, related_name='projects')
    is_deleted = models.BooleanField(verbose_name='удалено', null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время обновления')
    deleted_at = models.DateTimeField(verbose_name='Дата и время удаления', null=True, default=None)

    def __str__(self):
        return f'{self.name} - {self.description}'

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


