# 🧪 CRUD Employee API Test Automation Project (Allure + Pytest)

## 📦 Installing Dependencies

Before running the tests, make sure your virtual environment is activated and all required packages are installed:

1. Virtual environment:

    ```powershell (Windows)
   python -m venv .venv
   .\.venv\Scripts\Activate
   
    ```bash (Linux / macOS)
   python -m venv .venv
   source .venv/bin/activate

2. Required packages:

    ```bash / powershell
    pip install -r requirements.txt

## 🚀 Running Automated Tests with Allure Report (Windows)

### 📂 Шаги

1. Open PowerShell in the project directory.

2. Run the script:

   ```powershell 
    .\run.ps1
      
   ```bash 
   bash run.sh

# 📁 Test structure

crud_employee_allure/
├── employee.py              # API wrapper for interacting with the server
├── test_emplouees.py        # A set of automated tests for employees
├── run.ps1                  # PowerShell script to run tests and report
├── run.sh                   # Bash script to run tests and report
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation



