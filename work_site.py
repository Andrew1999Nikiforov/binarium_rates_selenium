from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from password import param
import time
from datetime import datetime
import socket
import re
from selenium.webdriver.common.keys import Keys

def start_program_y(): # Получаем строку из второй программы
    server_address = ('localhost', 14777)  # Укажите адрес и порт, на котором программа Y будет слушать
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(server_address)
        print("Ждем сообщение...")
        data, address = s.recvfrom(1024)
        param.text_sms = data.decode('utf-8')
        print("Сообщение от программы X:", param.text_sms)

def text_processing(message): # Функция которая обрабатывает строку с канала
    pattern = r'([A-Za-z]+)\s+(\d{2}:\d{2})\s+(вверх|вниз)'
    match = re.match(pattern, message)
    if match:
        param.active = match.group(1)
        param.time = match.group(2)
        param.up_or_down = match.group(3)
        return True
    else:
        return False

def change_real_money_to_game(driver): # Перевод счета с реального на игровой
    try: 
        WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.XPATH, '//div[@title="Баланс реального счета" and contains(text(), "Реальный")]'))).click()
        WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.wallet-account.--demo .wallet-account__button'))).click()
    except TimeoutException:
        print("Кнопка для перевода счета с реального на игровой не найдена за отведенное время.")

def is_time_difference_greater_than_5_minutes(time_str1, time_str2): # сравнение двух времени больше 5 минут или меньше
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

def check_input_is_empty(driver): # Проверяем поле для ввода акций пустая она или нет, если нет, то опустошаем
    try:
       input_text = WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Поиск актива"]'))).get_attribute("value")
       if input_text == "":
            return True
       else:
            input_text.clear()
    except TimeoutException:
        print("Кнопка для ввода акций не найдена")

def change_active_money(driver, active, time_t): # выбор активов слева сверху
    try:
        WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.XPATH, '//div[@class="chart-tab__content"]//div[@class="chart-tab__toggle"]'))).click()
        input_active = WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Поиск актива"]')))
        input_active.send_keys(Keys.BACK_SPACE * len(input_active.get_attribute("value")))
        input_active.send_keys(active)
        time.sleep(1)
        if change_long_or_short_active(time_t):
            elements = WebDriverWait(driver, param.timeout).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'asset-profit__score')))
            second_element = elements[1]
            second_element.click()
        else:
            WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'asset-profit__score'))).click()
    except TimeoutException:
        print("Кнопка для выбора % денег не найдена за отведенное время.")

def close_banner(driver): # Закрываем баннер с рекламой
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, '--color-light'))).click()
    except TimeoutException:
        print("Кнопка для закрытия банера не появилась")
        pass
    except NoSuchElementException:
        print("Кнопка для закрытия банера не появилась")
        pass

def close_banner_cookie(driver): # Закрываем баннер с куки
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Хорошо']"))).click()
    except TimeoutException:
        print("Кнопка для закрытия банера cookie не появилась")
        pass
    except NoSuchElementException:
        print("Кнопка для закрытия банера cookie не появилась")
        pass

def change_time(driver, time_t): # Установка времени 
    try:
        text_from_time = WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[a-test="currentExpiration"]'))).get_attribute("title")
        while text_from_time < time_t:
            WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.t-expiration-spinners .spinners__button.--inc'))).click()
            time.sleep(1)
            text_from_time = WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[a-test="currentExpiration"]'))).get_attribute("title")
    except TimeoutException:
        print("Кнопка времени не найдена")

def change_up_or_down(driver, up_or_down): # Выбор куда ставить вверх или вниз
    try:
        time.sleep(1)
        if up_or_down == "вверх":
            WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.CLASS_NAME, '--call'))).click()
        elif up_or_down == "вниз":
            WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.CLASS_NAME, '--put'))).click()
        time.sleep(30)
    except TimeoutException:
        print("Кнопка времени не найдена")