from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime
from password import param 
from password import active
import socket
import re
import time

def start_program_y(): # Получаем строку из второй программы
    server_address = ('localhost', 14777)  # Укажите адрес и порт, на котором программа Y будет слушать
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(server_address)
        print("Ждем сообщение...")
        data, address = s.recvfrom(1024)
        param.text_sms = data.decode('utf-8')

def check_slash_to_name_active(incoming_word): # проверка актива на то, имеется ли слэш в его названии например GPB/USD или EUR/USD
    for pair in active.mass_active_name_slash:
        if pair[0] == incoming_word:
            param.active = pair[1]

def text_processing(message): # Функция которая обрабатывает строку с канала либо новая ставка либо сигнал о результате
    pattern1 = r'^([A-Za-z\s()]+)\s+(\d+)\s+минут\s+(вверх|вниз|ВВЕРХ|ВНИЗ)$'
    pattern2 = r'^([A-Za-z\s()]+)\s+сигнал\s+в\s+(плюс|минус)$'
    match1 = re.match(pattern1, message)
    match2 = re.match(pattern2, message)
    if match1:
        param.active = match1.group(1)
        param.time = match1.group(2)
        param.up_or_down = match1.group(3)
        param.array2.append(param.active)
        check_slash_to_name_active(param.active)
        param.count_rate+=1
        return True
    elif match2:
        param.name_signal = match2.group(1)
        param.result_signal = match2.group(2)
        param.array_res.append(param.name_signal)
        param.count_signal+=1
        return True
    return False

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
            #time.sleep(0.1)
            check_availability = WebDriverWait(driver, param.timeout).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'asset-profit__score')))
            #check_availability = driver.find_elements(By.CLASS_NAME, "asset-profit__score")
            if len(check_availability) == 1:
                check_availability[0].click()
            else: 
                check_availability[1].click()
            return True
        else:
            WebDriverWait(driver, param.timeout).until(EC.presence_of_element_located((By.CLASS_NAME, 'asset-profit__score'))).click()
            return True
    except Exception as e:
        print(f"Кнопка для выбора % денег не найдена за отведенное время. Ошибка {e}")
        close_active_menu(driver)
        clear_input_text_change_active_money(driver)
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
