from rest_framework import serializers

from .models import Department, Employee, Position


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
        fields = ["department"]


class EmployeeDetailSerializer(serializers.ModelSerializer):
    position = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ["employee_id", "name", "surname", "position", "department"]

    def get_position(self, obj):
        try:
            position = Position.objects.get(employee_id=obj.employee_id)
            return position.position
        except Position.DoesNotExist:
            return None

    def get_department(self, obj):
        try:
            department = Department.objects.get(surname=obj.surname)
            return department.department
        except Department.DoesNotExist:
            return None


class EmployeeWithPositionAndDepartmentSerializer(serializers.ModelSerializer):
    position = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ["employee_id", "name", "surname", "position", "department"]

    def get_position(self, obj):
        try:
            position = Position.objects.get(employee_id=obj.employee_id)
            return position.position
        except Position.DoesNotExist:
            return None

    def get_department(self, obj):
        try:
            department = Department.objects.get(surname=obj.surname)
            return department.department
        except Department.DoesNotExist:
            return None
