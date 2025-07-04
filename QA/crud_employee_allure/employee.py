import requests
import os
import allure
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()


class EmployeeApi:
    def __init__(self, base_url):
        self.base_url = base_url

    @allure.step("API. Создание нового сотрудника")
    def create_employee(self, **kwargs):
        """Создание нового сотрудника"""
        url = f"{self.base_url}/employee/create"
        response = requests.post(url, json=kwargs, headers={"Content-Type": "application/json"})
        allure.attach(str(response.text), name="Ответ от API", attachment_type=allure.attachment_type.JSON)
        return response

    @allure.step("API. Получение информации о сотруднике по ID")
    def get_employee_info(self, employee_id):
        """Получение информации о сотруднике по ID"""
        url = f"{self.base_url}/employee/info/{employee_id}"
        response = requests.get(url)
        allure.attach(str(response.text), name="Ответ на получение информации", attachment_type=allure.attachment_type.JSON)
        return response

    @allure.step("API. Получение токена авторизации")
    def get_token(self):
        """Получить токен авторизации из .env"""
        creds = {
            "username": os.getenv("USER"),
            "password": os.getenv("PASSWORD")
        }

        response = requests.post(f"{self.base_url}/auth/login", json=creds)
        allure.attach(str(response.text), name="Ответ авторизации", attachment_type=allure.attachment_type.JSON)

        assert response.status_code == 200, f"Ожидался статус 200, получен: {response.status_code}"
        return response.json()["user_token"]

    @allure.step("API. Изменение данных сотрудника")
    def change_employee(self, employee_id, **kwargs):
        """Изменение данных сотрудника по ID"""
        client_token = self.get_token()
        url = f"{self.base_url}/employee/change/{employee_id}"
        params = {"client_token": client_token}

        response = requests.patch(url, params=params, json=kwargs)
        allure.attach(str(response.text), name="Ответ на изменение сотрудника", attachment_type=allure.attachment_type.JSON)

        if response.status_code != 200:
            raise Exception(f"Ошибка при обновлении сотрудника: {response.status_code}, {response.text}")
        return response


