from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db.models.fields import timezone


class MyUser(AbstractUser):
    pass


class Client(models.Model):
    client_name = models.CharField(max_length=35)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    # project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.client_name

class Project(models.Model):
    project_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.ManyToManyField(MyUser, related_name='user')

    def __str__(self):
        return self.project_name



