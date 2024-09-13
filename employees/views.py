from rest_framework import generics, status
from rest_framework.response import Response

from .models import Department, Employee, Position
from .serializers import (DepartmentSerializer, EmployeeDetailSerializer,
                          EmployeeSerializer,
                          EmployeeWithPositionAndDepartmentSerializer,
                          PositionSerializer)


class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class PositionListView(generics.ListAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class EmployeeDetailView(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeDetailSerializer
    lookup_field = "employee_id"


class EmployeeWithPositionAndDepartmentListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeWithPositionAndDepartmentSerializer


class EmployeeCreateView(generics.CreateAPIView):
    serializer_class = EmployeeSerializer

    def create(self, request, *args, **kwargs):
        employee_serializer = self.get_serializer(data=request.data)
        employee_serializer.is_valid(raise_exception=True)
        self.perform_create(employee_serializer)

        position_data = request.data.get("position")
        department_data = request.data.get("department")

        Position.objects.create(
            employee_id=employee_serializer.data["employee_id"], position=position_data
        )
        Department.objects.create(
            department=department_data,
            position=position_data,
            surname=employee_serializer.data["surname"],
        )

        return Response(employee_serializer.data, status=status.HTTP_201_CREATED)
