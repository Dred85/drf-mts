from django.core.management import BaseCommand

from employees.models import Department, Employee, Position


class Command(BaseCommand):
    help = "Заполняет таблицы данными (5 экземпляров для каждой таблицы)"

    def handle(self, *args, **options):
        # Создание 5 экземпляров сотрудников
        for i in range(5):
            Employee.objects.create(name=f"Имя_{i + 1}", surname=f"Фамилия_{i + 1}")

        # Создание 5 экземпляров должностей
        for i in range(5):
            Position.objects.create(position=f"Должность_{i + 1}")

        # Создание 5 экземпляров отделов
        for i in range(5):
            Department.objects.create(
                department=f"Отдел_{i + 1}",
                position=f"Должность_{(i % 5) + 1}",  # Указываем комбинацию должностей
                surname=f"Фамилия_{(i % 5) + 1}",  # Используем существующие фамилии
            )

        self.stdout.write(self.style.SUCCESS("Таблицы успешно заполнены данными."))
