from selenium import webdriver
import login_site
import work_site
import password
import manage_prog

driver = webdriver.Chrome() 

manage_prog.manage_programm_function(driver)

driver.quit()

