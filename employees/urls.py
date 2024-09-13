from django.urls import path

from .views import (DepartmentListView, EmployeeCreateView, EmployeeDetailView,
                    EmployeeListView,
                    EmployeeWithPositionAndDepartmentListView,
                    PositionListView)

urlpatterns = [
    path(
        "employees/", EmployeeListView.as_view(), name="employee-list"
    ),  # Получить список всех сотрудников
    path(
        "positions/", PositionListView.as_view(), name="position-list"
    ),  # Получить список всех должностей
    path(
        "departments/", DepartmentListView.as_view(), name="department-list"
    ),  # Получить список всех отделов
    path(
        "employee/<int:employee_id>/",
        EmployeeDetailView.as_view(),
        name="employee-detail",
    ),  # Получить данные сотрудника по id
    path(
        "employees-with-details/",
        EmployeeWithPositionAndDepartmentListView.as_view(),
        name="employee-list-with-details",
    ),  # Получить список сотрудников с должностью и отделом
    path("employee/add/", EmployeeCreateView.as_view(), name="employee-add"),
]  # Добавить сотрудника на существующую должность в отдел
