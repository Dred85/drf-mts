from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Department, Employee, Position
from .serializers import (DepartmentSerializer, EmployeeDetailSerializer,
                          EmployeeSerializer,
                          EmployeeWithPositionAndDepartmentSerializer,
                          PositionSerializer)


class EmployeeListView(generics.ListAPIView):
    """Get - Получить список всех сотрудников из таблицы: Employee"""

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer



class PositionListView(generics.ListAPIView):
    """Get - Получить список всех должностей из таблицы: Position"""

    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class DepartmentListView(generics.ListAPIView):
    """Get - Получить список уникальных отделов из таблицы Department"""

    serializer_class = DepartmentSerializer

    def get_queryset(self):
        # Возвращаем только уникальные отделы
        return Department.objects.all().distinct('department')


class EmployeeDetailView(generics.RetrieveAPIView):
    """Get - Получить данные одного сотрудника по ID"""

    serializer_class = EmployeeDetailSerializer
    queryset = Employee.objects.all()
    lookup_field = 'employee_id'

class EmployeeWithPositionAndDepartmentListView(generics.ListAPIView):
    """Get - Получить список всех сотрудников с должностью и отделом"""

    serializer_class = EmployeeSerializer

    def list(self, request, *args, **kwargs):
        employees = Employee.objects.all()
        employee_data = []

        for employee in employees:
            # Получаем все должности и отделы для сотрудника
            positions = Position.objects.filter(employee_id=employee.employee_id)
            departments = Department.objects.filter(surname=employee.surname)

            # Предполагаем, что у сотрудника может быть только одна должность и один отдел
            position = positions.first() if positions.exists() else None
            department = departments.first() if departments.exists() else None

            employee_data.append({
                "employee_id": employee.employee_id,
                "name": employee.name,
                "surname": employee.surname,
                "position": position.position if position else None,
                "department": department.department if department else None,
            })

        return Response(employee_data)


class EmployeeCreateView(generics.CreateAPIView):
    """Post - Добавить сотрудника с выбранной должностью и отделом, которые существуют"""

    serializer_class = EmployeeSerializer

    def create(self, request, *args, **kwargs):
        employee_serializer = self.get_serializer(data=request.data)
        employee_serializer.is_valid(raise_exception=True)

        # Получаем данные из запроса
        position_data = request.data.get("position")
        department_data = request.data.get("department")
        name = request.data.get("name")
        surname = request.data.get("surname")

        # Проверка на существование должности
        position = Position.objects.filter(position=position_data).first()
        if not position:
            raise ValidationError({"position": "Указана несуществующая должность."})

        # Проверка на существование отдела
        department = Department.objects.filter(department=department_data).first()
        if not department:
            raise ValidationError({"department": "Указан несуществующий отдел."})

        # Проверка на существование сотрудника с той же комбинацией имени и фамилии
        if Employee.objects.filter(name=name, surname=surname).exists():
            existing_employee = Employee.objects.get(name=name, surname=surname)
            raise ValidationError({"detail": f"Сотрудник с именем {name} и фамилией {surname} уже существует. ID: {existing_employee.employee_id}"})

        # Сохраняем сотрудника
        employee = employee_serializer.save()

        # Проверка на существование записи в таблице должностей
        if not Position.objects.filter(position=position_data, employee_id=employee.employee_id).exists():
            Position.objects.create(position=position_data, employee_id=employee.employee_id)

        # Проверка на существование записи в таблице отделов
        if not Department.objects.filter(department=department_data, position=position_data, surname=surname).exists():
            Department.objects.create(department=department_data, position=position_data, surname=surname)

        # Формируем ответ с данными сотрудника
        response_data = {
            "employee_id": employee.employee_id,
            "name": employee.name,
            "surname": employee.surname,
            "position": position.position,
            "department": department.department,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
