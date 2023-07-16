from django.db import models

# Create your models here.
class Participant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    regNum = models.CharField(max_length=100, unique=True)
    course = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    year = models.CharField(default=0, max_length=100)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.regNum
