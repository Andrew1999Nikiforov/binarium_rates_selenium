from selenium import webdriver
import manage_prog

driver = webdriver.Chrome() 

manage_prog.manage_programm_function(driver)

driver.quit()

