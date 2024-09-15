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
        fields = ["employee_id", "name", "surname"]


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ["position"]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["department"]


class EmployeeDetailSerializer(BaseEmployeeSerializer):
    position = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()


class EmployeeWithPositionAndDepartmentSerializer(BaseEmployeeSerializer):
    position = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()


class EmployeeCreateSerializer(serializers.ModelSerializer):
    position = serializers.CharField(write_only=True)
    department = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ["employee_id", "name", "surname", "position", "department"]

    def validate(self, data):
        name = data.get("name")
        surname = data.get("surname")
        position_data = data.get("position")
        department_data = data.get("department")

        # Вызываю валидатор из внешнего модуля
        validate_employee_data(name, surname, position_data, department_data)

        return data

    def create(self, validated_data):
        position_data = validated_data.pop("position")
        department_data = validated_data.pop("department")
        surname = validated_data.get("surname")

        # Создаем сотрудника
        employee = Employee.objects.create(**validated_data)

        # Используем get_or_create для позиций и отделов
        Position.objects.get_or_create(
            position=position_data, employee_id=employee.employee_id
        )

        Department.objects.get_or_create(
            department=department_data, position=position_data, surname=surname
        )

        return employee
