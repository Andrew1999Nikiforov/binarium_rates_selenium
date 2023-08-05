from selenium import webdriver
import login_site
import work_site
import time

driver = webdriver.Chrome() 
url = "https://binarium.win/ru/terminal"  

driver.get(url)

login_site.login(driver)
work_site.change_real_money_to_game(driver)
work_site.change_active_money(driver)
driver.quit()