from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
import time
import pymysql
import os
import configparser
import sshtunnel 
from sshtunnel import SSHTunnelForwarder
import re
caps = {
    'platformName': 'Android',
    'platformVersion': '12',
    'deviceName': 'IFS84POZMRKBHEQ8',
     "noReset" : True,
     "autoGrantPermissions": True,
     "unicodeKeyboard": False,  
     "resetKeyboard": True  
  }

driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)
driver.implicitly_wait(10)

config = configparser.ConfigParser()
# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
config_keyfile = os.path.join(current_dir, 'DB.ini')
# 讀取配置文件
config.read(config_keyfile, encoding='utf-8')

ssh_host=config.get('Host','ssh_host')
ssh_user=config.get('Host','ssh_user')
ssh_password=config.get('Host','ssh_password')
ssh_keyfile = os.path.join(current_dir, 'india-api-dev.pem')    
mysql_host=config.get('Host','mysql_host')
mysql_port=3306
mysql_user=config.get('Host','mysql_user')
mysql_password=config.get('Host','mysql_password')
mysql_database=config.get('Host','mysql_database')
packageid=config.get('Host','packageid')
phone_no=config.get('login','phone_no')



#輸入號碼
driver.find_element(By.ID, packageid + "phoneEditText").send_keys(phone_no)
print ("\033[32m輸入手機號 OK\033[0m")
time.sleep(5)
#點擊OTP鈕
driver.find_element(By.ID, packageid + "sendOtpTextView").click()
print ("\033[32m提交OTP OK\033[0m")
time.sleep(5)


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
        sql=f"SELECT content FROM hs_sms_record WHERE phone_no =  '{phone_no}'ORDER BY id DESC LIMIT 1"
        cursor.execute(sql)
        result=cursor.fetchall()
        time.sleep(3)

# 提取数字部分
if result:
    message = result[0][0].strip()  # 提取短信内容
    match = re.search(r'\b\d+\b', message)
    
    if match:
        extracted_number = match.group()
#帶入OTP碼        
driver.find_element(By.ID, packageid + "otpCodeEditText").send_keys(extracted_number)
print ("\033[32m帶入OTP碼 OK\033[0m")
#點擊confirm
driver.find_element(By.ID, packageid + "confirmTextView").click()
print ("\033[32m點擊confirm OK\033[0m")
time.sleep(3)

driver.find_element(By.ID, packageid + "ivPreviousPage").click()
time.sleep(3)
#點擊next鈕
driver.find_element(By.ID, packageid + "nextTextView").click()
time.sleep(1)
#輸入號碼
driver.find_element(By.ID, packageid + "phoneEditText").send_keys(phone_no)
time.sleep(2)
#點擊OTP鈕
driver.find_element(By.ID, packageid + "sendOtpTextView").click()

driver.quit()


