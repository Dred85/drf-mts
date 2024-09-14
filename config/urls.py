from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/", include("employees.urls")
    ),  # Подключение маршрутов из приложения employees
]
