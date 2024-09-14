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
    """Get - Получить список всех отделов из таблицы: Department"""

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class EmployeeDetailView(generics.RetrieveAPIView):
    """Get - Получить данные одного сотрудника по id (Имя, Фамилия, Должность, Отдел)"""

    queryset = Employee.objects.all()
    serializer_class = EmployeeDetailSerializer
    lookup_field = "employee_id"


class EmployeeWithPositionAndDepartmentListView(generics.ListAPIView):
    """Get - Получить список всех сотрудников (id, Имя, Фамилия, Должность, Отдел)"""

    queryset = Employee.objects.all()
    serializer_class = EmployeeWithPositionAndDepartmentSerializer


class EmployeeCreateView(generics.CreateAPIView):
    """Post - Добавить сотрудника на существующую должность в существующий отдел"""

    serializer_class = EmployeeSerializer

    def create(self, request, *args, **kwargs):
        employee_serializer = self.get_serializer(data=request.data)
        employee_serializer.is_valid(raise_exception=True)

        # Получаем данные из запроса
        position_data = request.data.get("position")
        department_data = request.data.get("department")

        # Проверка на существование должности
        try:
            position = Position.objects.get(position=position_data)
        except Position.DoesNotExist:
            raise ValidationError({"position": "Указана несуществующая должность."})

        # Проверка на существование отдела
        try:
            department = Department.objects.get(department=department_data, position=position_data)
        except Department.DoesNotExist:
            raise ValidationError({"department": "Указан несуществующий отдел."})

        # Если проверки пройдены, создаю нового сотрудника
        self.perform_create(employee_serializer)

        return Response(employee_serializer.data, status=status.HTTP_201_CREATED)
