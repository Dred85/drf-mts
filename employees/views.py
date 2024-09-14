from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

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

    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class DepartmentListView(generics.ListAPIView):
    """Get - Получить список уникальных отделов из таблицы Department"""

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

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
