from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime
from password import param
from password import active
import socket
import re

def start_program_y(): # Получаем строку из второй программы
    server_address = ('localhost', 14777)  # Укажите адрес и порт, на котором программа Y будет слушать
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(server_address)
        print("Ждем сообщение...")
        data, address = s.recvfrom(1024)
        param.text_sms = data.decode('utf-8')

def remove_slash(input_string): # в Регулярных выражениях убирает знак / и заменяет на пробел
    return input_string.replace("/", " ")

def add_slash(input_string):
    return input_string.replace(" ", "/")

def text_processing(message): # Функция которая обрабатывает строку с канала
    pattern = r'([\w\s\(\)]+)\s+((?:вверх|вниз|ВВЕРХ|ВНИЗ))\s+(\d{2}:\d{2})'
    #message = check_name_active(message)
    message = remove_slash(message)
    match = re.match(pattern, message)
    if match:
        param.active = match.group(1)
        param.up_or_down = match.group(2)
        param.time = match.group(3)
        param.active = add_slash(param.active)
        return True
    else:
        return False

def check_name_active(text_without_slash): # Функция которая добавляет знак / в слова из словаря active
    if text_without_slash in active.active:
        return(text_without_slash[:3] + '/' + text_without_slash[3:])


def change_real_money_to_game(driver): # Перевод счета с реального на игровой
    try: 
        WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.XPATH, '//div[@title="Баланс реального счета" and contains(text(), "Реальный")]'))).click()
        WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.wallet-account.--demo .wallet-account__button'))).click()
    except Exception as e:
        print(f"Кнопка для перевода счета с реального на игровой не найдена за отведенное время. Ошибка {e}")

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

def close_active_menu(driver): # Закрываем баннер с рекламой
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, '--color-dark'))).click()
    except Exception as e:
        print(f"Кнопка для закрытия банера актив меню не появилась. Ошибка {e}")

def clear_input_text_change_active_money(driver):
    try:
        WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.XPATH, '//div[@class="chart-tab__content"]//div[@class="chart-tab__toggle"]'))).click()
        input_active = WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Поиск актива"]')))
        input_active.send_keys(Keys.BACK_SPACE * len(input_active.get_attribute("value")))
        close_active_menu(driver)
    except Exception as e:
        print(f"Очистка строки для ввода акций не удалась. Ошибка {e}")
        close_active_menu(driver)

def change_active_money(driver, active, time_t): # выбор активов слева сверху
    try:
        WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.XPATH, '//div[@class="chart-tab__content"]//div[@class="chart-tab__toggle"]'))).click()
        WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Поиск актива"]'))).send_keys(active)
        if change_long_or_short_active(time_t):
            WebDriverWait(driver, param.timeout).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'asset-profit__score')))[1].click()
            return True
        else:
            WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'asset-profit__score'))).click()
            return True
    except Exception as e:
        print(f"Кнопка для выбора % денег не найдена за отведенное время. Ошибка {e}")
        close_active_menu(driver)
        return False

def close_banner(driver): # Закрываем баннер с рекламой
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, '--color-light'))).click()
    except Exception as e:
        print(f"Кнопка для закрытия банера не появилась. Ошибка {e}")

def close_banner_cookie(driver): # Закрываем баннер с куки
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Хорошо']"))).click()
    except Exception as e:
        print(f"Кнопка для закрытия банера cookie не появилась. Ошибка {e}")

def change_time(driver, time_t): # Установка времени 
    try:
        text_from_time = WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[a-test="currentExpiration"]'))).get_attribute("title")
        while text_from_time < time_t:
            WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.t-expiration-spinners .spinners__button.--inc'))).click()
            text_from_time = WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[a-test="currentExpiration"]'))).get_attribute("title")
    except Exception as e:
        print(f"Кнопка для установки времени не найдена. Ошибка {e}")

def change_up_or_down(driver, up_or_down): # Выбор куда ставить вверх или вниз
    try:
        if up_or_down == "вверх":
            WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.CLASS_NAME, '--call'))).click()
        elif up_or_down == "вниз":
            WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.CLASS_NAME, '--put'))).click()
    except Exception as e:
        print(f"Кнопка для выбора куда ставить вверх или вниз не найдена. Ошибка {e}")
