#!/bin/bash

# Очистка предыдущих результатов
rm -rf allure-results allure-report

# Запуск тестов с генерацией результатов для Allure
pytest --alluredir=allure-results

# Генерация отчёта
allure generate allure-results -o allure-report --clean

# Открытие отчёта в браузере
allure open allure-report
