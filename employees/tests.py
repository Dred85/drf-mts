from rest_framework import status
from rest_framework.test import APITestCase

from .models import Department, Employee, Position


class EmployeeTestCase(APITestCase):

    def setUp(self) -> None:
        # Создаем должности и отделы
        self.position1 = Position.objects.create(position="Должность_1")
        self.position2 = Position.objects.create(position="Должность_2")

        self.department1 = Department.objects.create(
            department="Отдел_1", position="Должность_1", surname="Иванов"
        )
        self.department2 = Department.objects.create(
            department="Отдел_2", position="Должность_2", surname="Петров"
        )

        # Создаем сотрудников
        self.employee1 = Employee.objects.create(name="Иван", surname="Иванов")
        self.employee2 = Employee.objects.create(name="Петр", surname="Петров")

    def test_get_employee_list(self):
        """Тест получения списка всех сотрудников"""
        response = self.client.get("/api/employees/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)  # У нас два сотрудника в базе

    def test_get_position_list(self):
        """Тест получения списка всех должностей"""
        response = self.client.get("/api/positions/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)  # У нас две должности в базе

    def test_get_department_list(self):
        """Тест получения списка всех отделов"""
        response = self.client.get("/api/departments/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)  # У нас два отдела в базе

    def test_get_single_employee(self):
        """Тест получения данных одного сотрудника по id"""
        response = self.client.get(f"/api/employee/{self.employee1.pk}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_employee_detailed_list(self):
        """Тест получения списка всех сотрудников с id, именем, фамилией, должностью и отделом"""
        response = self.client.get("/api/employees-with-details/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_employee(self):
        """Тестирование успешного создания сотрудника"""
        data = {
            "name": "Роберто",
            "surname": "Карлос",
            "position": "Должность_1",
            "department": "Отдел_1",
        }
        response = self.client.post("/api/employee/add/", data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_employee_non_existent_department(self):
        """Тестирование создания сотрудника с несуществующим отделом"""
        data = {
            "name": "Роберто",
            "surname": "Карлос",
            "position": "Должность_1",
            "department": "Несуществующий_отдел",
        }
        response = self.client.post("/api/employee/add/", data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Указан несуществующий отдел.", response.json().get("department", "")
        )

    def test_create_employee_non_existent_position(self):
        """Тестирование создания сотрудника с несуществующей должностью"""
        data = {
            "name": "Роберто",
            "surname": "Карлос",
            "position": "Несуществующая_должность",
            "department": "Отдел_1",
        }
        response = self.client.post("/api/employee/add/", data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Указана несуществующая должность.", response.json().get("position", "")
        )
