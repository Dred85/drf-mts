from rest_framework.exceptions import ValidationError

from .models import Department, Employee, Position


def validate_employee_data(name, surname, position_data, department_data):
    # Проверка на существование сотрудника с той же комбинацией имени и фамилии
    if Employee.objects.filter(name=name, surname=surname).exists():
        raise ValidationError(
            f"Сотрудник с именем {name} и фамилией {surname} уже существует."
        )

    # Проверка на существование должности
    position = Position.objects.filter(position=position_data).first()
    if not position:
        raise ValidationError({"position": "Указана несуществующая должность."})

    # Проверка на существование отдела
    department = Department.objects.filter(department=department_data).first()
    if not department:
        raise ValidationError({"department": "Указан несуществующий отдел."})

    return position, department
