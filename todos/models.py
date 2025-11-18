from django.db import models


# Create your models here.
class ToDo(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.TextField()
