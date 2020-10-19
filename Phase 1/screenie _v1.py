# https://selenium-python.readthedocs.io/installation.html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PIL import Image
from io import BytesIO
import time

driver = webdriver.Firefox()
driver.maximize_window()
driver.get("https://www.google.com/maps")
time.sleep(10)

#search jayanagar
search = driver.find_element_by_id('searchboxinput')
search.clear()
search.send_keys('Jayanagar')
search.send_keys(Keys.RETURN)
time.sleep(7)
    
hamburger = driver.find_element_by_class_name('searchbox-hamburger')
hamburger.click()
time.sleep(7)

#set satellite on
sat = driver.find_element_by_xpath("//div[@class='widget-settings-earth-item']/child::button[1]")
if(sat.get_attribute('aria-checked') == 'false'):
    sat.click()
time.sleep(4)

hamburger.click()
time.sleep(3)

label_off = driver.find_element_by_xpath("//div[@class='widget-settings-earth-item']/child::button[2]/child::label[2]")
driver.execute_script("arguments[0].style.display = 'inline'", label_off)

#set map on
map = driver.find_element_by_xpath("//ul[@class='widget-settings-list']/child::li[1]/child::button[1]")
if(map.get_attribute('aria-checked') == 'false'):
    map.click()
time.sleep(4)

hamburger.click()
time.sleep(3)

#get labels to show
label_container = driver.find_element_by_xpath("//div[@class='widget-settings-earth-item']/child::button[2]")
driver.execute_script("arguments[0].style.display = 'inline'", label_container)

#click on label
label_off.click()


time.sleep(15)

print("successful")
driver.quit()

