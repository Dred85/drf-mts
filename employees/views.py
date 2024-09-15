from rest_framework import generics

from .models import Department, Employee, Position
from .serializers import (DepartmentSerializer, EmployeeCreateSerializer,
                          EmployeeDetailSerializer, EmployeeSerializer,
                          EmployeeWithPositionAndDepartmentSerializer,
                          PositionSerializer)


class EmployeeListView(generics.ListAPIView):
    """Get - Получить список всех сотрудников из таблицы: Employee"""

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class PositionListView(generics.ListAPIView):
    """Get - Получить список всех должностей из таблицы: Position"""

    queryset = Position.objects.all().distinct("position")
    serializer_class = PositionSerializer


class DepartmentListView(generics.ListAPIView):
    """Get - Получить список уникальных отделов из таблицы Department"""

    queryset = Department.objects.distinct("department")
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        # Возвращаем только уникальные отделы
        return Department.objects.all().distinct("department")


class EmployeeDetailView(generics.RetrieveAPIView):
    """Get - Получить данные одного сотрудника по ID"""

    serializer_class = EmployeeDetailSerializer
    queryset = Employee.objects.all()
    lookup_field = "employee_id"


class EmployeeWithPositionAndDepartmentListView(generics.ListAPIView):
    """Get - Получить список всех сотрудников с должностью и отделом"""

    serializer_class = EmployeeWithPositionAndDepartmentSerializer
    queryset = Employee.objects.all()


class EmployeeCreateView(generics.CreateAPIView):
    """Post - Добавить сотрудника с выбранной должностью и отделом, которые существуют"""

    serializer_class = EmployeeCreateSerializer

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        position_data = validated_data.pop("position")
        department_data = validated_data.pop("department")
        surname = validated_data.get("surname")

        # Создаем сотрудника
        employee = Employee.objects.create(**validated_data)

        # Используем get_or_create для создания должностей и отделов
        Position.objects.get_or_create(
            position=position_data, employee_id=employee.employee_id
        )

        Department.objects.get_or_create(
            department=department_data, position=position_data, surname=surname
        )

        return employee
