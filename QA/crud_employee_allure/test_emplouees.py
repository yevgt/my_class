import pytest
import allure
from employee import EmployeeApi

BASE_URL = "http://5.101.50.27:8000"


@pytest.fixture
def api():
    return EmployeeApi(BASE_URL)


@allure.epic("Сотрудники")
@allure.severity(allure.severity_level.CRITICAL)
class TestEmployeeAPI:

    @allure.id("EMP-001")
    @allure.feature("Создание")
    @allure.story("Создание нового сотрудника")
    @allure.title("Создание сотрудника: Peter First")
    @allure.description("Создание сотрудника с валидными данными. Проверяются все ключевые поля в ответе.")
    def test_create_employee(self, api):
        with allure.step("Формируем данные для сотрудника Peter First"):
            payload = {
                "first_name": "Peter",
                "last_name": "First",
                "middle_name": "M",
                "company_id": 1,
                "email": "peter.first@example.com",
                "phone": "+1234567890",
                "birthdate": "2000-01-01"
            }

        with allure.step("Отправляем запрос на создание сотрудника"):
            response = api.create_employee(**payload)
            assert response.status_code == 200
            data = response.json()
            allure.attach(str(data), name="Ответ API", attachment_type=allure.attachment_type.JSON)

        with allure.step("Проверяем корректность полей в ответе"):
            for key, expected in payload.items():
                assert data[key] == expected, f"{key}: ожидалось {expected}, получено {data[key]}"
            assert "id" in data, "В ответе отсутствует поле 'id'"

    @allure.id("EMP-002")
    @allure.feature("Чтение")
    @allure.story("Получение информации по сотруднику")
    @allure.title("Запрос данных сотрудника: Bob Cat")
    @allure.description("Создание и последующее извлечение данных сотрудника по его ID.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_employee_info(self, api):
        with allure.step("Создаём Bob для теста"):
            response = api.create_employee(
                first_name="Bob",
                last_name="Cat",
                middle_name="M",
                company_id=2,
                email="bob.cat@example.com",
                phone="+1234567654",
                birthdate="2001-02-02"
            )
            assert response.status_code == 200
            employee_id = response.json()["id"]

        with allure.step(f"Получаем информацию о сотруднике ID={employee_id}"):
            resp = api.get_employee_info(employee_id)
            assert resp.status_code == 200
            info = resp.json()
            allure.attach(str(info), name="Информация о сотруднике Bob Cat", attachment_type=allure.attachment_type.JSON)

        with allure.step("Проверяем ключевые поля"):
            assert info["id"] == employee_id
            assert info["first_name"] == "Bob"

    @allure.id("EMP-003")
    @allure.feature("Обновление")
    @allure.story("Редактирование сотрудника")
    @allure.title("Обновление данных сотрудника: Hanz Second → Nosecond")
    @allure.description("Создание, обновление и валидация изменения данных сотрудника.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_change_employee(self, api):
        with allure.step("Создаём Hanz Second"):
            response = api.create_employee(
                first_name="Hanz",
                last_name="Second",
                middle_name="M",
                company_id=3,
                email="hanz.second@example.com",
                phone="+1987654321",
                birthdate="1999-11-11",
                is_active=True
            )
            assert response.status_code == 200
            employee_id = response.json()["id"]

        with allure.step("Обновляем сотрудника Second → Nosecond"):
            updated_resp = api.change_employee(
                employee_id,
                last_name="Nosecond",
                email="hanz.nosecond@example.com",
                phone="+1245433467",
                is_active=True
            )
            assert updated_resp.status_code == 200
            updated = updated_resp.json()
            allure.attach(str(updated), name="Обновлённые данные", attachment_type=allure.attachment_type.JSON)

        with allure.step("Проверяем изменения в полях"):
            assert updated["last_name"] == "Nosecond", f"Ожидалось 'Nosecond', получено '{updated['last_name']}'"
            assert updated["email"] == "hanz.nosecond@example.com", \
        f"Ожидалось 'hanz.nosecond@example.com', получено '{updated['email']}'"
            assert updated["phone"] == "+1245433467", f"Ожидалось '+1245433467', получено '{updated['phone']}'"
            assert updated["is_active"] is True, f"Ожидалось 'True' '{updated['is_active']}'"

