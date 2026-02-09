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
    with open('table_1702887158620.txt', 'r', encoding='utf-8') as file:
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
#-------------------------------------------------------------------------------
#1. 訪客首頁
elements = driver.find_elements(By.XPATH, "//*[@clickable='true']")
if elements:
    for _ in range(4):  # 循环点击四次
        for element in elements:
            try:
                element.click()
                time.sleep(0.5)
            except Exception as e:
                print(f"Failed to click: {e}")
time.sleep(5)
x1, y1 = 343, 1253   ## 起始位置
x2, y2 = 343, 276    ## 終點位置
action = TouchAction(driver)
for _ in range(2):
	action.press(x=x1, y=y1).wait(200).move_to(x=x2, y=y2).release().perform()
driver.find_element(By.XPATH, "//*[contains(@text, 'Agree')]").click()
time.sleep(5)
x1, y1 = 343, 1253   ## 起始位置
x2, y2 = 343, 276    ## 終點位置
action = TouchAction(driver)
for _ in range(5):
	action.press(x=x1, y=y1).wait(250).move_to(x=x2, y=y2).release().perform()
driver.find_element(By.XPATH, "//*[contains(@text, 'Agree')]").click()
time.sleep(2)
element = driver.find_element(By.XPATH, "//*[contains(@text, 'Payment')]")
element.click()
print('1. 訪客首頁  \033[32mOK\033[0m')
time.sleep(0.5)
#2. 登入頁
#輸入號碼
elements = driver.find_elements(By.XPATH, "//*[@clickable='true']")
if elements:
    target_element = elements[1]
    target_element.click()
    target_element.send_keys(phone_no)
#點擊OTP鈕
elements = driver.find_elements(By.XPATH, "//*[@clickable='true']")
if elements:
    elements[3].click()
time.sleep(2)
#DB資料(更換DB(IN2).ini & india-api-product.pem)-------------------------------------------------------
# 創建configparser
config = configparser.ConfigParser()
# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
config_keyfile = os.path.join(current_dir, 'DB(IN2).ini')
# 讀取配置文件
config.read(config_keyfile)

ssh_host=config.get('Hosts','ssh_host')
ssh_user=config.get('Hosts','ssh_user')
ssh_password=config.get('Hosts','ssh_password')
ssh_keyfile = os.path.join(current_dir, 'india-api-product.pem')    

mysql_host=config.get('Hosts','mysql_host')
mysql_port=3306
mysql_user=config.get('Hosts','mysql_user')
mysql_password=config.get('Hosts','mysql_password')
mysql_database=config.get('Hosts','mysql_database')

with SSHTunnelForwarder(
    ssh_host,
    ssh_username=ssh_user,
    ssh_password=ssh_password,
    ssh_pkey=ssh_keyfile,
    remote_bind_address=(mysql_host,mysql_port),
    local_bind_address=('localhost',3307)
)as server:
    conn=pymysql.connect(
        host='localhost',
        port=server.local_bind_port,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )
    with conn.cursor() as cursor:
        sql=f"SELECT content FROM hs_sms_record WHERE phone_no = '{phone_no}' ORDER BY id DESC LIMIT 1"
        cursor.execute(sql)
        result=cursor.fetchall()
        time.sleep(3)
#關閉DB連接
conn.close()
# 提取数字部分
if result:
    message = result[0][0].strip()  # 提取短信内容
    match = re.search(r'\b\d+\b', message)
    
    if match:
        extracted_number = match.group()


#帶入OTP碼        
elements = driver.find_elements(By.XPATH, "//*[@clickable='true']")
if elements:
    target_element = elements[2]
    target_element.click()
    target_element.send_keys(extracted_number)
#點擊confirm
driver.find_element(By.ID, package + confirmTextView).click()
print('2. 登入頁 \033[32mOK\033[0m')
time.sleep(10)
#3. 未認證首頁
driver.find_element(By.ID, package + btnApply).click()
print('3. 未認證首頁 \033[32mOK\033[0m')
#4. let's go
elements = driver.find_elements(By.XPATH, "//android.widget.TextView")
if elements:
    elements[11].click()
time.sleep(1)
driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.Button[1]").click()
driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[3]/android.widget.Button[1]").click()
driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.Button[1]").click()
driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.Button[1]").click()
driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.Button[1]").click()
print('4. lets go \033[32mOK\033[0m')
#5. person infor
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[0].click()
driver.find_element(By.XPATH, "//android.widget.TextView").click()
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[1].click()
driver.find_element(By.XPATH, "//android.widget.TextView").click()
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[2].click()
driver.find_element(By.XPATH, "//android.widget.TextView").click()
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[3].click()
driver.find_element(By.XPATH, "//android.widget.TextView").click()
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[4].send_keys("sdfd@dd.dd")
driver.find_element(By.XPATH, "//*[contains(@text, 'Next')]").click()
time.sleep(5)
print('5. person infor \033[32mOK\033[0m')
#6. Contact
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[0].click()
driver.find_element(By.XPATH, "//android.widget.TextView").click()
element = driver.find_element(By.XPATH, "//*[contains(@text, 'Dd')]")
element.click()
time.sleep(1)
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[3].click()
driver.find_element(By.XPATH, "//android.widget.TextView").click()
element = driver.find_element(By.XPATH, "//*[contains(@text, 'Dig')]")
element.click()
driver.find_element(By.XPATH, "//*[contains(@text, 'Next')]").click()
time.sleep(2)
print('6. Contact \033[32mOK\033[0m')
#7. QA
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[0].click()
driver.find_element(By.XPATH, "//android.widget.TextView").click()
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[1].click()
driver.find_element(By.XPATH, "//android.widget.TextView").click()
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[2].click()
driver.find_element(By.XPATH, "//android.widget.TextView").click()
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[3].click()
driver.find_element(By.XPATH, "//android.widget.TextView").click()
driver.find_element(By.XPATH, "//*[contains(@text, 'Next')]").click()
time.sleep(2)
print('7. QA \033[32mOK\033[0m')
#8. ID
elements = driver.find_elements(By.XPATH, "//*[@clickable='true']")
if elements:
    elements[1].click()
time.sleep(1)
driver.find_element(By.ID, package + imageCaptureButton).click()
time.sleep(1)
driver.find_element(By.ID, package + confirmTextView).click()
time.sleep(1)
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[0].send_keys("sdfde1234s")
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[1].send_keys("sdfde1234s")
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[3].send_keys("sdfde1234s")
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[2].click()
x1, y1 = 206, 733   ## 起始位置
x2, y2 = 206, 1480    ## 終點位置
action = TouchAction(driver)
for _ in range(3):
	action.press(x=x1, y=y1).wait(1000).move_to(x=x2, y=y2).release().perform()
driver.find_element(By.XPATH, "//*[contains(@text, 'OK')]").click()
elements = driver.find_elements(By.XPATH, "//android.widget.TextView")
if elements:
    last_element = elements[-1]
    last_element.click()
time.sleep(1)
elements = driver.find_elements(By.XPATH, "//*[@clickable='true']")
if elements:
    elements[2].click()
time.sleep(1)
driver.find_element(By.ID, package + imageCaptureButton).click()
time.sleep(1)
driver.find_element(By.ID, package + confirmTextView).click()
time.sleep(3)
driver.find_element(By.XPATH, "//*[contains(@text, 'Next')]").click()
time.sleep(8)
print('8. ID \033[32mOK\033[0m')
#9. bank
elements = driver.find_elements(By.CLASS_NAME, 'android.widget.EditText')
if elements:
    elements[1].send_keys("12345673289")
elements = driver.find_elements(By.CLASS_NAME, 'android.widget.EditText')
if elements:
    elements[2].send_keys("12345673289")
elements = driver.find_elements(By.CLASS_NAME, 'android.widget.EditText')
if elements:
    elements[3].send_keys("asdf0126785")
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
driver.tap([(370, 1037)])
time.sleep(5)
print('9. bank \033[32mOK\033[0m')
#10. 額度模型
driver.find_element(By.XPATH, "//*[contains(@text, 'Cancel')]").click()
elements = driver.find_elements(By.CLASS_NAME, 'android.widget.TextView')
if elements:
    last_element = elements[-1]
    last_element.click()
elements = driver.find_elements(By.CLASS_NAME, 'android.widget.TextView')
if elements:
    elements[2].click()
time.sleep(2)
print('10. 額度模型 \033[32mOK\033[0m')