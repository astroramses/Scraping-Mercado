import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
import pathlib
from dbfread import DBF
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import requests
import csv
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


#######################
#Subo los archivos dbf#
#######################

def check_exists_by_xpath(vab):
    try:
        driver.find_element(By.XPATH, (vab))
    except NoSuchElementException:
        return False
    return True

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.implicitly_wait(10)
driver.get("https://tienda.mercadolibre.com.co/golty")

resultadoTotal=int(str(driver.find_element(By.XPATH,"//span[@class='ui-search-search-result__quantity-results shops-custom-secondary-font']").text)[:-11])

data = pd.DataFrame(index=list(range(0,300)))
data["PRODUCTOS"] =  0
data["PRECIOS"] =  0

numeroPaginas = int(str(driver.find_element(By.CLASS_NAME, "andes-pagination__page-count").text)[3:])

resultadoUltima = resultadoTotal - ((resultadoTotal//48)*48)

ayudaContador = 0

for k in list(range(0,48)):
            data.iloc[ayudaContador,0] = driver.find_elements(By.XPATH, "//h2[@class='ui-search-item__title ui-search-item__group__element shops__items-group-details shops__item-title']")[k].text 
            data.iloc[ayudaContador,1] = driver.find_elements(By.XPATH, "//div[@class='ui-search-price ui-search-price--size-medium shops__price']/div[1]/span[1]/span[1]")[k].text 
            ayudaContador = ayudaContador + 1
for i in list(range(0,numeroPaginas-1)):
    time.sleep(1)
    ayudaSiguiente = driver.find_element(By.XPATH, "//a[@title='Siguiente']").get_attribute('href')
    driver.get(ayudaSiguiente)
    if(i == numeroPaginas-2):
        for j in list(range(0,resultadoUltima)):
            data.iloc[ayudaContador,0] = driver.find_elements(By.XPATH, "//h2[@class='ui-search-item__title ui-search-item__group__element shops__items-group-details shops__item-title']")[j].text 
            data.iloc[ayudaContador,1] = driver.find_elements(By.XPATH, "//div[@class='ui-search-price ui-search-price--size-medium shops__price']/div[1]/span[1]/span[1]")[j].text 
            ayudaContador = ayudaContador + 1 
    else:
        for j in list(range(0,48)):
            data.iloc[ayudaContador,0] = driver.find_elements(By.XPATH, "//h2[@class='ui-search-item__title ui-search-item__group__element shops__items-group-details shops__item-title']")[j].text 
            data.iloc[ayudaContador,1] = driver.find_elements(By.XPATH, "//div[@class='ui-search-price ui-search-price--size-medium shops__price']/div[1]/span[1]/span[1]")[j].text 
            ayudaContador = ayudaContador + 1 

data.to_excel("output.xlsx")

    

