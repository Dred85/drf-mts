from django.db import models

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Position(models.Model):
    id = models.AutoField(primary_key=True)
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.position

class Department(models.Model):
    id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=100)  # Название
    position = models.CharField(max_length=100)  # Должность
    last_name = models.CharField(max_length=100)  # Фамилия

    class Meta:
        unique_together = ('name', 'last_name')

    def __str__(self):
        return f"{self.department} - {self.last_name}"
