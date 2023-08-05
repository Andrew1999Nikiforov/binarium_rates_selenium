from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from password import param
import time
from datetime import datetime

def change_real_money_to_game(driver): # Перевод счета с реального на игровой
    try: 
        WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.XPATH, '//div[@title="Баланс реального счета" and contains(text(), "Реальный")]'))).click()
        WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.wallet-account.--demo .wallet-account__button'))).click()
    except TimeoutException:
        print("Кнопка для перевода счета с реального на игровой не найдена за отведенное время.")

def is_time_difference_greater_than_5_minutes(time_str1, time_str2): # сравнение двух времени 
    time_format = '%H:%M'
    time1 = datetime.strptime(time_str1, time_format)
    time2 = datetime.strptime(time_str2, time_format)
    time_diff_seconds = abs((time2 - time1).total_seconds())
    return time_diff_seconds > 5 * 60

def change_long_or_short_active(time_sms): # выбор % в активах !!!!time_sms в формате 15:00 должно быть
    current_time = datetime.now().strftime('%H:%M')
    if is_time_difference_greater_than_5_minutes(current_time, time_sms): #!!!time_sms в формате 15:00 должно быть
        return True
    else:
        return False

def change_active_money(driver): # выбор активов слева сверху
    try:
        WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.XPATH, '//div[@class="chart-tab__content"]//div[@class="chart-tab__toggle"]'))).click()
        input_active = WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Поиск актива"]')))
        input_active.send_keys("LATAM")
        time.sleep(1)
        if change_long_or_short_active("21:20"):
            elements = WebDriverWait(driver, param.timeout).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'asset-profit__score')))
            second_element = elements[1]
            second_element.click()
        else:
            WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'asset-profit__score'))).click()
    except TimeoutException:
        print("Кнопка для выбора % денег не найдена за отведенное время.")

def change_time(driver):
    try:
        text_from_time = WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[a-test="currentExpiration"]'))).get_attribute("title")
        while text_from_time < "21:20":
            WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.t-expiration-spinners .spinners__button --inc'))).click()
    except TimeoutException:
        print("Кнопка времени не найдена")