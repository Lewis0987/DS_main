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
import mysql.connector
from selenium.common.exceptions import NoSuchElementException
from colorama import Fore, Style
caps = {
    'platformName': 'Android',
    'platformVersion': '12',
    'deviceName': '3445796886005RU',
     "noReset" : True,
     "autoGrantPermissions": True,
     "unicodeKeyboard": False,  
     "resetKeyboard": True  
  }

driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)
driver.implicitly_wait(10)

#ini檔配置
config = configparser.ConfigParser()
current_dir = os.path.dirname(os.path.abspath(__file__))
config_keyfile = os.path.join(current_dir, 'IN DEV.ini')
config.read(config_keyfile, encoding='utf-8')
exit = config.get('texts','exit')
stay = config.get('texts','stay')
otp = config.get('login','otp')



config = configparser.ConfigParser()
current_dir = os.path.dirname(os.path.abspath(__file__)) # 获取当前文件所在目录的绝对路径
config_keyfile = os.path.join(current_dir, 'DB配置.ini')
config.read(config_keyfile, encoding='utf-8')            # 讀取配置文件
ssh_host=config.get('IND_dev','ssh_host')
ssh_user=config.get('IND_dev','ssh_user')
ssh_password=config.get('IND_dev','ssh_password')
ssh_keyfile = os.path.join(current_dir, 'india-api-dev.pem')    
mysql_host=config.get('IND_dev','mysql_host')
mysql_port=3306
mysql_user=config.get('IND_dev','mysql_user')
mysql_password=config.get('IND_dev','mysql_password')
mysql_database=config.get('IND_dev','mysql_database')
packageid=config.get('IND_dev','packageid')


db = mysql.connector.connect(
    host= "india-api-dev.ck0p8hows6ib.ap-south-1.rds.amazonaws.com", # MySQL 伺服器地址 
    user="okusr",
    password="3mWZ3BhdVFQDOjG4MKWy", #你的密碼
    database="in-api-dev"     #您要連接的數據庫名
)

# 創建游標對象
cursor = db.cursor()

# 執行 SQL 查詢
query = "SELECT otp FROM okdatabase.hs_sms_record WHERE user_id = %s ORDER BY timestamp DESC LIMIT 1;"
#指定用戶ID
phone_no = '9999999999' ##指定用戶ID
cursor.execute(query, (phone_no,))

# 獲取查詢結果
result = cursor.fetchone()

if result:
    otp = result[0]
    print(f"獲取的 OTP 為: {otp}")
else:
    print("找不到 OTP 記錄")

#找到OTP欄位並輸入OTP值
driver.find_element(By.ID, "com.ind.kyc.application:id/otpCodeEditText").click()
otp_value = '123456'
otp_element = driver.find_element(By.ID, "com.ind.kyc.application:id/otpCodeEditText")
otp_element.send_keys(otp_value)
# 關閉游標和數據庫連接
cursor.close()
db.close()
