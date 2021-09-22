

from django.db import models

class Employee(models.Model):
    eno = models.IntegerField(primary_key=True)
    ename = models.CharField(max_length=30)
    salary = models.IntegerField()
    email = models.EmailField(max_length=254, unique=True,null=True,blank=True)

    def __str__(self):
        return self.email
