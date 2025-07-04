import pytest
from employee import EmployeeApi

BASE_URL = "http://5.101.50.27:8000"

@pytest.fixture
def api():
    return EmployeeApi(BASE_URL)


def test_create_employee(api):
    response = api.create_employee(
        first_name="Peter",
        last_name="First",
        middle_name="M",
        company_id=1,
        email="peter.first@example.com",
        phone="+1234567890",
        birthdate="2000-01-01"
    )

    data = response.json()
    print(data)

    assert response.status_code == 200, f"Expected 200 Created, got {response.status_code}"
    assert "id" in data, "Response JSON should contain 'id'"
    assert data["first_name"] == "Peter", f"Ожидалось 'Peter', получено '{data['first_name']}'"
    assert data["last_name"] == "First", f"Ожидалось 'First', получено '{data['last_name']}'"
    assert data["middle_name"] == "M", f"Ожидалось 'M', получено '{data['middle_name']}'"
    assert data["company_id"] == 1, f"Ожидалось 1, получено {data['company_id']}"
    assert data["email"] == "peter.first@example.com", (f"Ожидалось 'peter.first@example.com', "
                                                          f"получено '{data['email']}'")
    assert data["phone"] == "+1234567890", f"Ожидалось '+1234567890', получено '{data['phone']}'"
    assert data["birthdate"] == "2000-01-01", f"Ожидалось '2000-01-01', получено '{data['birthdate']}'"


def test_get_employee_info(api):
    # Предварительно создаем сотрудника для теста
    create_resp = api.create_employee(
        first_name="Bob",
        last_name="Cat",
        middle_name="M",
        company_id=2,
        email="bob.cat@example.com",
        phone="+1234567654",
        birthdate="2001-02-02"
    )
    assert create_resp.status_code == 200
    employee_id = create_resp.json()["id"]

    resp = api.get_employee_info(employee_id)

    info = resp.json()
    print(info)

    assert resp.status_code == 200
    assert info["id"] == employee_id
    assert info["first_name"] == "Bob", f"Ожидалось 'Bob', получено '{info['first_name']}'"


def test_change_employee(api):
    # Создаем сотрудника
    create_resp = api.create_employee(
        first_name="Hanz",
        last_name="Second",
        middle_name="M",
        company_id=3,
        email="hanz.second@example.com",
        phone="+1987654321",
        birthdate="1999-11-11",
        is_active=True
    )

    assert create_resp.status_code == 200
    employee_id = create_resp.json()["id"]
    print("Employee ID:", employee_id)

    # Обновляем данные
    resp = api.change_employee(
        employee_id,
        last_name="Nosecond",
        email="hanz.nosecond@example.com",
        phone="+1245433467",
        is_active=True
    )

    updated_info = resp.json()
    print(updated_info)

    assert resp.status_code == 200
    assert updated_info["last_name"] == "Nosecond", f"Ожидалось 'Nosecond', получено '{updated_info['last_name']}'"
    assert updated_info["email"] == "hanz.nosecond@example.com", \
        f"Ожидалось 'hanz.nosecond@example.com', получено '{updated_info['email']}'"
    assert updated_info["phone"] == "+1245433467", f"Ожидалось '+1245433467', получено '{updated_info['phone']}'"
    assert updated_info["is_active"] is True, f"Ожидалось 'True' '{updated_info['is_active']}'"
