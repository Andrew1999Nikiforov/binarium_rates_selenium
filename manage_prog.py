from selenium import webdriver
import login_site
import work_site
import password
import manage_prog

def manage_programm_function(driver):
    driver.get(password.param.url)
    login_site.login(driver)
    work_site.change_real_money_to_game(driver)
    work_site.close_banner(driver)
    work_site.close_banner_cookie(driver)

    while True:
        work_site.start_program_y()
        if work_site.text_processing(password.param.text_sms):
            if work_site.change_active_money(driver, password.param.active, password.param.time):
                work_site.change_time(driver, password.param.time)
                work_site.change_up_or_down(driver, password.param.up_or_down)
            else:
                continue
        else:
            continue