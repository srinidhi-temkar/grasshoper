# https://selenium-python.readthedocs.io/installation.html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PIL import Image
from io import BytesIO
import time

with open('wards.txt', 'r') as f:
    c = [line.strip() for line in f]

driver = webdriver.Firefox()

def open_maps():
    #open window
    driver.maximize_window()
    driver.get("https://www.google.com/maps")
    time.sleep(4)

def search_place(ward_name):
    search = driver.find_element_by_id('searchboxinput')
    search.clear()
    search.send_keys(ward_name)
    search.send_keys(Keys.RETURN)
    time.sleep(2)
    
def show_satellite():
    open_hamburger()
    #set satellite on
    sat = driver.find_element_by_xpath("//div[@class='widget-settings-earth-item']/child::button[1]")
    if(sat.get_attribute('aria-checked') == 'false'):
        sat.click()
    time.sleep(3)

def show_outline():
    open_hamburger()
    #set attribute of 'Labels off' to 'display:inline'
    label_off = driver.find_element_by_xpath("//div[@class='widget-settings-earth-item']/child::button[2]/child::label[2]")
    driver.execute_script("arguments[0].style.display = 'inline'", label_off)

    #switch to map
    my_map = driver.find_element_by_xpath("//ul[@class='widget-settings-list']/child::li[1]/child::button[1]")
    if(my_map.get_attribute('aria-checked') == 'false'):
        my_map.click()
    time.sleep(2)

    open_hamburger()
    #don't show terrain!
    terrain = driver.find_element_by_xpath("//ul[@class='widget-settings-list']/child::li[3]/child::button[1]")
    if(terrain.get_attribute('aria-checked') == 'false'):
        terrain.click()
    time.sleep(2)
    #and get rid of that pesky widget
    terrain_widget = driver.find_element_by_xpath("//div[@class='app-center-widget-holder']")
    driver.execute_script("arguments[0].style.display = 'none'", terrain_widget)
    
    open_hamburger()
    #get labels under satellite to show
    label_container = driver.find_element_by_xpath("//div[@class='widget-settings-earth-item']/child::button[2]")
    driver.execute_script("arguments[0].style.display = 'inline'", label_container)
    #click on label
    label_off.click()
    time.sleep(2)
    
def remove_labels():
    open_hamburger()
    #Remove labels
    sat_label = driver.find_element_by_xpath("//div[@class='widget-settings-earth-item']/child::button[2]")
    if(sat_label.get_attribute('aria-checked') == 'true'):
        sat_label.click()
    time.sleep(2)

def take_screenshot(screenshot_name): 
    png = driver.get_screenshot_as_png()
    im = Image.open(BytesIO(png))

    #crop
    width, height = im.size    # Get dimensions
    left = 5 * width/14
    top = height/20
    right = 9 * width/10
    bottom = 19 * height/20
    cropped_im = im.crop((left, top, right, bottom))
    cropped_im.save(screenshot_name)

def open_hamburger():
    hamburger = driver.find_element_by_class_name('searchbox-hamburger')
    hamburger.click()
    time.sleep(2)

if __name__ == "__main__":
    
    i = 1
    open_maps()
    for ele in c:
        ward = ele + ", Bangalore"
        filename_of_outline = str(i) + " outline " + ele + ".png"
        filename_of_satellite = str(i) + " " + ele + ".png"

        search_place(ward)
        print(ward, end = '\t')
        
        show_satellite()
        remove_labels()
        take_screenshot(filename_of_satellite)
        print(filename_of_satellite, end = '\t')

        show_outline()
        take_screenshot(filename_of_outline)
        print(filename_of_outline)

        i+=1
