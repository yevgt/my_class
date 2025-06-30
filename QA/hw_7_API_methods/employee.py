import requests
import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

class EmployeeApi:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_employee(self, **kwargs):
        """Создание нового сотрудника"""
        url = f"{self.base_url}/employee/create"

        resp = requests.post(url, json=kwargs, headers={"Content-Type": "application/json"})
        return resp

    def get_employee_info(self, employee_id):
        """Получение информации о сотруднике по ID с использованием URL"""
        url = f"{self.base_url}/employee/info/{employee_id}"
        resp = requests.get(url)
        return resp

    def get_token(self):
        """Получить токен авторизации"""
        creds = {
            "username": os.getenv("USER"),
            "password": os.getenv("PASSWORD")
        }
        resp = requests.post(self.base_url + '/auth/login', json=creds)
        assert resp.status_code == 200, f"Ошибка: ожидался статус 200, получен {resp.status_code}"
        return resp.json()["user_token"]

    def change_employee(self, employee_id, **kwargs):
        """Изменение данных о сотруднике по ID"""
        client_token = self.get_token()

        # Формируем URL с employee_id
        url = f"{self.base_url}/employee/change/{employee_id}"

        # Добавляем client_token в параметры запроса
        params = {'client_token': client_token}

        resp = requests.patch(url, params=params, json=kwargs)

        if resp.status_code != 200:
            raise Exception(f"Ошибка при изменении сотрудника: статус {resp.status_code}, ответ: {resp.text}")
        return resp