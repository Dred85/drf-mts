from rest_framework import serializers

from .models import Department, Employee, Position
from .validators import validate_employee_data


class BaseEmployeeSerializer(serializers.ModelSerializer):
    position = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ["employee_id", "name", "surname", "position", "department"]

    @staticmethod
    def get_position(obj):
        position = Position.objects.filter(employee_id=obj.employee_id).first()
        return position.position if position else None

    @staticmethod
    def get_department(obj):
        department = Department.objects.filter(surname=obj.surname).first()
        return department.department if department else None


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ["position"]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["department"]


class EmployeeDetailSerializer(BaseEmployeeSerializer):
    pass


class EmployeeWithPositionAndDepartmentSerializer(BaseEmployeeSerializer):
    pass


class EmployeeCreateSerializer(serializers.ModelSerializer):
    position = serializers.CharField(
        write_only=True
    )  # дополнительное поле, не связано напрямую с моделью Employee
    department = serializers.CharField(
        write_only=True
    )  # дополнительное поле, не связано напрямую с моделью Employee

    class Meta:
        model = Employee
        fields = ["employee_id", "name", "surname", "position", "department"]

    def validate(self, data):
        # из входных данных извлекаем нужную информацию
        name = data.get("name")
        surname = data.get("surname")
        position_data = data.get("position")
        department_data = data.get("department")

        # Вызываю валидатор из внешнего модуля
        validate_employee_data(name, surname, position_data, department_data)

        return data
