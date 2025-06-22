from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OverviewPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_total_amount(self):
        total_label = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label")))
        return total_label.text.split("$")[-1].strip()

    def finish_checkout(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "finish"))).click()
