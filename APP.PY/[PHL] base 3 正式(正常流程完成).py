from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymysql
import os
import configparser
from sshtunnel import SSHTunnelForwarder
import re
from selenium.common.exceptions import NoSuchElementException
import pytz
from datetime import datetime, timedelta
from Method import print_marquee
from selenium.common.exceptions import TimeoutException
import time
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
    with open('table_1702524953437.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if search_text in line:
                parts = line.strip().split('R.id.')
                resource_id = parts[-1].split()[-1]
                break
    return resource_id

normalBtnViewApply = get_resource_id('R.id.normalBtnViewApply')
confirmTextView = get_resource_id('R.id.confirmTextView')
cancelTextView = get_resource_id('R.id.cancelTextView')
#i18n.ini(更換i18n(IN).ini內部的[package] & [phone_no])------------------------------------------------------------------------
config = configparser.ConfigParser()
# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
config_keyfile = os.path.join(current_dir, 'i18n(PHL).ini')
# 讀取配置文件
config.read(config_keyfile, encoding='utf-8')

package = config.get('basic','package')
phone_no= config.get('basic','phone_no')

#1. 訪客首頁
element = driver.find_element(By.XPATH, "//*[contains(translate(@text, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'skip')]")
element.click()
time.sleep(5)
x1, y1 = 348, 1110   ## 起始位置
x2, y2 = 348, 155    ## 終點位置
action = TouchAction(driver)
for _ in range(2):
	action.press(x=x1, y=y1).wait(100).move_to(x=x2, y=y2).release().perform()
driver.find_element(By.XPATH, "//*[contains(@text, 'Agree')]").click()
time.sleep(5)
x1, y1 = 348, 1110   ## 起始位置
x2, y2 = 348, 155    ## 終點位置
action = TouchAction(driver)
for _ in range(2):
	action.press(x=x1, y=y1).wait(100).move_to(x=x2, y=y2).release().perform()
driver.find_element(By.XPATH, "//*[contains(@text, 'Agree')]").click()
try:
    # 等待元素出现并点击
    element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(@text, 'Payment')]"))
    )
    element.click()
except TimeoutException:
    # 如果在5秒内未找到元素，跳过操作
    pass
print('1. 訪客首頁  \033[32mOK\033[0m')
#2. 登入頁
#輸入號碼
element = driver.find_element(By.XPATH, "//*[@text='Enter Your phone number']")
element.click()
element.send_keys(phone_no)
#點擊OTP鈕
element = driver.find_element(By.XPATH, "//*[@text='Get OTP']")
element.click()
time.sleep(2)
#DB資料(更換DB(IN2).ini & india-api-product.pem)-------------------------------------------------------
# 創建configparser
config = configparser.ConfigParser()
# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
config_keyfile = os.path.join(current_dir, 'DB(PHL)-1.ini')
# 讀取配置文件
config.read(config_keyfile)

ssh_host=config.get('Hosts','ssh_host')
ssh_user=config.get('Hosts','ssh_user')
ssh_password=config.get('Hosts','ssh_password')
ssh_keyfile = os.path.join(current_dir, 'ph-api-product.pem')    

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
elements = driver.find_elements(By.XPATH, "//*[contains(@text,'OTP Verification Code')]")
if elements:
    elements[1].click()
    elements[1].send_keys(extracted_number)
#點擊confirm
element = driver.find_element(By.XPATH, "//*[contains(@text,'Confirm')]")
element.click()
print('2. 登入頁 \033[32mOK\033[0m')
#3. 未認證首頁
try:
    # 等待元素出现并点击
    element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, package + normalBtnViewApply))
    )
    element.click()
except TimeoutException:
    # 如果在5秒内未找到元素，跳过操作
    pass
print('3. 未認證首頁 \033[32mOK\033[0m')
#4. let's go
driver.find_element(By.ID, package + confirmTextView).click()
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
    elements[2].send_keys("wsefefrf@sdf.ss")
driver.find_element(By.XPATH, "//android.widget.TextView").click()
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[3].click()
driver.find_element(By.XPATH, "//android.widget.TextView").click()
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[4].click()
driver.find_element(By.XPATH, "//android.widget.TextView").click()
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[5].send_keys("wsefefrf@sdf.ss")
elements = driver.find_elements(By.CLASS_NAME, 'android.widget.TextView')
if elements:
    last_element = elements[-1]
    last_element.click()
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
elements = driver.find_elements(By.CLASS_NAME, 'android.widget.TextView')
if elements:
    last_element = elements[-1]
    last_element.click()
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
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[4].click()
driver.find_element(By.XPATH, "//android.widget.TextView").click()
time.sleep(2)
elements = driver.find_elements(By.CLASS_NAME, 'android.widget.TextView')
if elements:
    last_element = elements[-1]
    last_element.click()
print('7. QA \033[32mOK\033[0m')
print("\033[91m" +"請手動操作"+ "\033[0m")
element = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(@text, 'Payment Method')]"))
    )

print('8. 手動ID \033[32mOK\033[0m')
time.sleep(2)
#9. bank
driver.tap([(630, 600)])
driver.tap([(300, 700)])

elements = driver.find_elements(By.XPATH, "//*[@clickable='true']")
if elements:
    last_element = elements[-3]
    last_element.send_keys("01111111111")
elements = driver.find_elements(By.XPATH, "//*[@clickable='true']")
if elements:
    last_element = elements[-2]
    last_element.send_keys("01111111111")
time.sleep(1)
driver.find_element(By.XPATH, "//*[@class='android.widget.Button']").click()
time.sleep(1)
driver.tap([(500, 1020)])
time.sleep(0.5)
driver.tap([(350, 1000)])
print('9. bank \033[32mOK\033[0m')
#10. 額度模型
driver.find_element(By.ID, package + cancelTextView).click()
driver.find_element(By.ID, package + confirmTextView).click()
driver.find_element(By.ID, package + cancelTextView).click()
time.sleep(2)
print('10. 額度模型 \033[32mOK\033[0m')
driver.quit()