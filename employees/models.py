from django.db import models


class Employee(models.Model):
    """Модель, описывающая имя и фамилию сотрудника"""

    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        verbose_name="Имя сотрудника",
        help_text="Укажите имя сотрудника",
    )
    surname = models.CharField(
        max_length=100,
        verbose_name="Фамилия сотрудника",
        help_text="Укажите фамилию сотрудника",
    )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def __str__(self):
        return f"{self.name} {self.surname}"


class Position(models.Model):
    """Модель, описывающая должность сотрудника"""

    employee_id = models.AutoField(primary_key=True)
    position = models.CharField(
        max_length=150,
        verbose_name="Должность сотрудника",
        help_text="Укажите должность сотрудника",
    )

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"

    def __str__(self):
        return self.position


class Department(models.Model):
    """Модель, описывающая отдел, где работает сотрудник"""

    department = models.CharField(
        max_length=150,
        verbose_name="Название департамента",
        help_text="Укажите название департамента",
    )

    position = models.CharField(
        max_length=150,
        verbose_name="Должность сотрудника",
        help_text="Укажите должность сотрудника",
    )

    surname = models.CharField(
        max_length=150,
        verbose_name="Фамилия сотрудника",
        help_text="Укажите фамилию сотрудника",
    )

    class Meta:
        verbose_name = "Отдел"
        verbose_name_plural = "Отделы"
        unique_together = ("position", "surname")  # Уникальная связь должность-фамилия

    def __str__(self):
        return f"{self.department}:{self.position} - {self.surname}"
