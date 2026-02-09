from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import os
import configparser

config = configparser.ConfigParser()
# 启动 Chromedriver
driver = webdriver.Chrome()
################新安卓單(請輸入)###########################
url = "https://log.xu-jie-tech.com/login?msg=LOGGED_OUT"
################新安卓單(請輸入)###########################
driver.get(url)
WebDriverWait(driver, 10)

#alart_event 檢查元素是否存在
try:
    alert_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(@data-test-subj, 'toastCloseButton')]"))
    )
    print("alart_event is clickable: \033[32mTrue\033[0m")
    # 可點擊元素執行任何其他操作
    alert_button.click()
except Exception as e:
    print("alart_event is not clickable: \033[31mFalse\033[0m", e)
    # 當無法點擊或找不到元素印錯誤訊息
#關閉alert
alert_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(@data-test-subj, 'toastCloseButton')]"))
)
alert_button.click()
print ("\033[33m關閉alart OK\033[0m") 

#--------------------------------------------------------------------------------------------------------------
#帳號
username_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(@data-test-subj, 'loginUsername')]"))
)
username_field.send_keys("elastic")
print('1.帳號  \033[32mOK\033[0m')
#密碼
password_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(@data-test-subj, 'loginPassword')]"))
)
password_field.send_keys("njhq9RPmzI4KlFpW41jld1pAi0Lltr1J")
print("2.密碼  \033[32mOK\033[0m")
#登入
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".css-1km4ln8-euiButtonDisplayContent"))
)
login_button.click()
print("3.登入  \033[32mOK\033[0m")
#登入_關閉alert
alert_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(@data-test-subj, 'toastCloseButton')]"))
)
alert_button.click()
print ("\033[33m關閉alart OK\033[0m")
sleep(2)
#已登入_選項Xujie
driver.find_element(By.XPATH, "//*[contains(@data-test-subj, 'space-card-default')]").click()
print ('4.選項Xujie \033[32mOK\033[0m')
sleep(5)
#登入_關閉alert
alert_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(@data-test-subj, 'toastCloseButton')]"))
)
alert_button.click()
print ("\033[33m關閉alart OK\033[0m")
sleep(1)
#側欄位_menu
sidemenu_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(@data-icon-type, 'menu')]"))
)
sidemenu_button.click()
print ('5.側欄位_menu \033[32mOK\033[0m')
sleep(1)
#側欄位_Discover
sidemeun_Discover = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(@href, 'https://log.xu-jie-tech.com/app/discover#/')]"))
)
sidemeun_Discover.click()
print ('6.側欄位_Discover \033[32mOK\033[0m')
sleep(5)
#搜尋欄位
driver.find_element(By.XPATH, "//*[contains(@data-test-subj, 'queryInput')]").send_keys('9999999999')
print ('7.Sendkey_9999999999 \033[32mOK\033[0m')
sleep(3)
#搜尋欄位送出
driver.find_element(By.XPATH, "//*[contains(@data-test-subj, 'querySubmitButton')]").click()
print ('8.Send_9999999999 \033[32mOK\033[0m')
#menu收合_Available_fields
sidemenu_Availablefields = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(@data-test-subj, 'field-@timestamp-showDetails')]"))
)
sidemenu_Availablefields.click()
print ('9.側欄位_menu收合_Available_fields \033[32mOK\033[0m')
#menu_Popular fields_add_app
sidemenu_Popular_fields_add_app = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(@data-test-subj, 'fieldToggle-app')]"))
)
sidemenu_Popular_fields_add_app.click()
print ('10.側欄位_Popular fields_add_app \033[32mOK\033[0m')
#menu_Popular fields_add_country
sidemenu_Popular_fields_add_country = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(@data-test-subj, 'fieldToggle-country')]"))
)
sidemenu_Popular_fields_add_country.click()
print ('11.側欄位_Popular fields_add_country \033[32mOK\033[0m')
#menu_Popular fields_add_message
sidemenu_Popular_fields_add_message = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(@data-test-subj, 'fieldToggle-message')]"))
)
sidemenu_Popular_fields_add_message.click()
print ('12.側欄位_Popular fields_add_message \033[32mOK\033[0m')
#menu_Popular fields_add_user.phone
sidemenu_Popular_fields_add_userphone = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(@data-test-subj, 'fieldToggle-user.phone')]"))
)
sidemenu_Popular_fields_add_userphone.click()
print ('13.側欄位_Popular fields_add_userphone \033[32mOK\033[0m')
input('Press Enter to exit...')



