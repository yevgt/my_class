# run.ps1
Remove-Item -Recurse -Force allure-results, allure-report -ErrorAction SilentlyContinue
pytest --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure open allure-report
