from selenium import webdriver
import login_site
import work_site

driver = webdriver.Chrome() 
url = "https://binarium.win/ru/terminal"  

driver.get(url)

login_site.login(driver)
work_site.change_real_money_to_game(driver)
work_site.change_active_money(driver)
work_site.change_time(driver)
work_site.change_up_or_down(driver)
driver.quit()