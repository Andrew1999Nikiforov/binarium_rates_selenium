import time
from password import param
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from password import password

def login(driver):# Вход в аккаунт
    try: 
        WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.ID, "mat-tab-link-2"))).click()
        WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.ID, "mat-input-3"))).send_keys(password.login_binarium)
        WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.ID, "mat-input-4"))).send_keys(password.password_binarium)
        WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.ID, "mat-checkbox-4"))).click()
        WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.XPATH, f"//button[@class='c-base-button' and text()='Войти']"))).click()
        print("Кнопка логинизации найдена!")
    except TimeoutException:
        print("Кнопка для авторизации на сайте не найдена.")