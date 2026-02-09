from appium import webdriver
from selenium.webdriver.common.by import By
import time
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymysql
import os
import configparser
import sshtunnel 
from sshtunnel import SSHTunnelForwarder
import re
from selenium.common.exceptions import NoSuchElementException
import pytz
from datetime import datetime, timedelta
#裝置設定(更改deviceName & platformVersion) -------------------------------------------------------------------------------
caps = {
	"platformName" : "Android",
	"deviceName": "3453270245006KH",
	"platformVersion": "12",
	"noReset" : True,
	"autoGrantPermissions": True,
	'unicodeKeyboard': True,  
    'resetKeyboard': True,
	'automationName': "UiAutomator2",
	}
driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)
driver.implicitly_wait(10)
#置換mapping ID(更換table.txt)------------------------------------------------------------------------
def get_resource_id(search_text):
    resource_id = ''
    with open('table_1702881303465.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if search_text in line:
                parts = line.strip().split('R.id.')
                resource_id = parts[-1].split()[-1]
                break
    return resource_id

btnApply = get_resource_id('R.id.btnApply')
confirmTextView = get_resource_id('R.id.confirmTextView')
titleTextView = get_resource_id('R.id.titleTextView')
nextTextView = get_resource_id('R.id.nextTextView')
scanPanImageView = get_resource_id('R.id.scanPanImageView')
imageCaptureButton = get_resource_id('R.id.imageCaptureButton')
iconImageView = get_resource_id('R.id.iconImageView')
faceImageView = get_resource_id('R.id.faceImageView')
cancelTextView=get_resource_id('R.id.cancelTextView')
#i18n.ini(更換i18n(IN).ini內部的[package] & [phone_no])------------------------------------------------------------------------
config = configparser.ConfigParser()
# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
config_keyfile = os.path.join(current_dir, 'i18n(IN).ini')
# 讀取配置文件
config.read(config_keyfile, encoding='utf-8')

package = config.get('basic','package')
phone_no= config.get('basic','phone_no')

#9. bank
elements = driver.find_elements(By.CLASS_NAME, 'android.widget.EditText')
if elements:
    elements[1].send_keys("9999999888")
elements = driver.find_elements(By.CLASS_NAME, 'android.widget.EditText')
if elements:
    elements[2].send_keys("9999999888")
elements = driver.find_elements(By.CLASS_NAME, 'android.widget.EditText')
if elements:
    elements[3].send_keys("aabb0888888")
time.sleep(1)
elements = driver.find_elements(By.CLASS_NAME, 'android.widget.EditText')
if elements:
	elements[4].click()
if elements:
    elements[4].send_keys("SF1@FGG")
time.sleep(3)   
##點擊confirm
driver.find_element(By.CLASS_NAME, 'android.widget.Button').click()
driver.find_element(By.CLASS_NAME, 'android.widget.Button').click()
time.sleep(5)
driver.tap([(533, 1627)])
time.sleep(5)
print('9. bank \033[32mOK\033[0m')
#10. 額度模型
driver.find_element(By.ID, package + cancelTextView).click()
driver.find_element(By.ID, package + confirmTextView).click()
driver.find_element(By.ID, package + cancelTextView).click()
time.sleep(2)
print('10. 額度模型 \033[32mOK\033[0m')