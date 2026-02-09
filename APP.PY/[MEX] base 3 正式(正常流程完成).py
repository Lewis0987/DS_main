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
    with open('table_1704262742320.txt', 'r', encoding='utf-8') as file:
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
config_keyfile = os.path.join(current_dir, 'i18n(MEX).ini')
# 讀取配置文件
config.read(config_keyfile, encoding='utf-8')

package = config.get('basic','package')
phone_no= config.get('basic','phone_no')

#1. 訪客首頁
for _ in range(2):
    elements = driver.find_elements(By.XPATH, "//*[@clickable='true']")
    if elements:
        elements[0].click()
        time.sleep(1)  # 每次点击后等待一段时间
    else:
        break  # 如果找不到元素，跳出循环
elements = driver.find_elements(By.XPATH, "//*[@clickable='true']")
if elements:
    elements[0].click()
time.sleep(3)
x1, y1 = 380, 1280   ## 起始位置
x2, y2 = 380, 500    ## 終點位置
action = TouchAction(driver)
for _ in range(2):
	action.press(x=x1, y=y1).wait(100).move_to(x=x2, y=y2).release().perform()
driver.find_element(By.XPATH, "//*[contains(@text, 'Aceptar')]").click()
time.sleep(3)
x1, y1 = 380, 1280   ## 起始位置
x2, y2 = 380, 500    ## 終點位置
action = TouchAction(driver)
for _ in range(2):
	action.press(x=x1, y=y1).wait(100).move_to(x=x2, y=y2).release().perform()
driver.find_element(By.XPATH, "//*[contains(@text, 'Aceptar')]").click()
time.sleep(2)
element = driver.find_element(By.XPATH, "//*[contains(@text, 'Pago')]")
element.click()
time.sleep(1)
print('1. 訪客首頁  \033[32mOK\033[0m')
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
config_keyfile = os.path.join(current_dir, 'DB(MEX).ini')
# 讀取配置文件
config.read(config_keyfile)

ssh_host=config.get('Hosts','ssh_host')
ssh_user=config.get('Hosts','ssh_user')
ssh_password=config.get('Hosts','ssh_password')
ssh_keyfile = os.path.join(current_dir, 'mx-api-product.pem')    

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
elements = driver.find_elements(By.XPATH, "//*[@clickable='true']")
if elements:
    elements[4].click()
print('2. 登入頁 \033[32mOK\033[0m')
#3. 未認證首頁
time.sleep(10)
driver.find_element(By.ID, package + normalBtnViewApply).click()
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
    elements[1].send_keys("wsefefrf@sdf.ss")
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
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[5].click()
x1, y1 = 501, 733   ## 起始位置
x2, y2 = 501, 1480    ## 終點位置
action = TouchAction(driver)
for _ in range(3):
	action.press(x=x1, y=y1).wait(1000).move_to(x=x2, y=y2).release().perform()
driver.find_element(By.XPATH, "//*[contains(@text, 'Aceptar')]").click()
time.sleep(3)
x1, y1 = 347, 1217   ## 起始位置
x2, y2 = 347, 400    ## 終點位置
action = TouchAction(driver)
action.press(x=x1, y=y1).wait(2000).move_to(x=x2, y=y2).release().perform()
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
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[5].click()
driver.find_element(By.XPATH, "//android.widget.TextView").click()
x1, y1 = 347, 1217   ## 起始位置
x2, y2 = 347, 400    ## 終點位置
action = TouchAction(driver)
action.press(x=x1, y=y1).wait(1000).move_to(x=x2, y=y2).release().perform()
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[4].click()
driver.find_element(By.XPATH, "//android.widget.TextView").click()
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[5].send_keys("wsefefrf")
driver.find_element(By.XPATH, "//android.widget.TextView").click()
elements = driver.find_elements(By.XPATH, "//android.widget.EditText")
if elements:
    elements[6].send_keys("wsefefrf")
driver.find_element(By.XPATH, "//android.widget.TextView").click()
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
        EC.presence_of_element_located((By.XPATH, "//*[contains(@text, 'Información bancaria')]"))
    )

print('8. 手動ID \033[32mOK\033[0m')
time.sleep(2)
#9. bank
elements = driver.find_elements(By.XPATH, "//*[@clickable='true']")
if elements:
    last_element = elements[-3]
    last_element.send_keys("1111333322224444")
elements = driver.find_elements(By.XPATH, "//*[@clickable='true']")
if elements:
    last_element = elements[-2]
    last_element.send_keys("1111333322224444")
elements = driver.find_elements(By.XPATH, "//*[@clickable='true']")
if elements:
    last_element = elements[-4]
    last_element.click()
time.sleep(0.5)
driver.press_keycode(4)
driver.tap([(370, 1037)])
driver.find_element(By.CLASS_NAME, 'android.widget.Button').click()
time.sleep(1)
elements = driver.find_elements(By.CLASS_NAME, 'android.widget.Button')
if elements:
    elements[2].click()
time.sleep(0.5)
driver.tap([(370, 1037)])
print('9. bank \033[32mOK\033[0m')
#10. 額度模型
driver.find_element(By.ID, package + cancelTextView).click()
driver.find_element(By.ID, package + confirmTextView).click()
driver.find_element(By.ID, package + cancelTextView).click()
time.sleep(2)
print('10. 額度模型 \033[32mOK\033[0m')
driver.quit()