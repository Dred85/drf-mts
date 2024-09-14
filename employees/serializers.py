from rest_framework import serializers

from .models import Department, Employee, Position
from .validators import validate_employee_data


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["employee_id", "name", "surname"]


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ["employee_id", "position"]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["department", "position", "surname"]


class EmployeeDetailSerializer(serializers.ModelSerializer):
    position = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ["employee_id", "name", "surname", "position", "department"]

    @staticmethod
    def get_position(obj):
        try:
            # Используем filter для получения всех позиций сотрудника
            position = Position.objects.filter(employee_id=obj.employee_id).first()
            return position.position if position else None
        except Position.DoesNotExist:
            return None

    @staticmethod
    def get_department(obj):
        try:
            # Используем filter вместо get для получения всех отделов по фамилии
            department = Department.objects.filter(surname=obj.surname).first()
            return department.department if department else None
        except Department.DoesNotExist:
            return None


class EmployeeWithPositionAndDepartmentSerializer(serializers.ModelSerializer):
    position = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ["employee_id", "name", "surname", "position", "department"]

    @staticmethod
    def get_position(obj):
        try:
            # Используем filter для получения всех позиций сотрудника
            position = Position.objects.filter(employee_id=obj.employee_id).first()
            return position.position if position else None
        except Position.DoesNotExist:
            return None

    @staticmethod
    def get_department(obj):
        try:
            # Используем filter вместо get для получения всех отделов по фамилии
            department = Department.objects.filter(surname=obj.surname).first()
            return department.department if department else None
        except Department.DoesNotExist:
            return None


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

        # Проверка на существование записи в таблице должностей
        if not Position.objects.filter(
                position=position_data, employee_id=employee.employee_id
        ).exists():
            Position.objects.create(
                position=position_data, employee_id=employee.employee_id
            )

        # Проверка на существование записи в таблице отделов
        if not Department.objects.filter(
                department=department_data, position=position_data, surname=surname
        ).exists():
            Department.objects.create(
                department=department_data, position=position_data, surname=surname
            )

        return employee
