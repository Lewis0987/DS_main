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

#ini檔配置
config = configparser.ConfigParser()
current_dir = os.path.dirname(os.path.abspath(__file__))
config_keyfile = os.path.join(current_dir, 'DB資料.ini')
config.read(config_keyfile, encoding='utf-8')
exit = config.get('texts','exit')
stay = config.get('texts','stay')
otp = config.get('otps','otp')
host = config.get('Hosts','host') 
phone_no = config.get('login','phone_no')

# 連接到 MySQL 數據庫
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
otp_element = driver.find_element_by_(By.ID, "com.ind.kyc.application:id/gnuivDncAeyq")
otp_element.send_keys(otp_value)
# 關閉游標和數據庫連接
cursor.close()
db.close()
