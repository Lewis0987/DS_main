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
from colorama import Fore, Style

caps = {
    'platformName': 'Android',
    'platformVersion': '12',
    'deviceName': '3445796886005RU', #oppo[IFS84POZMRKBHEQ8] vivo[3445796886005RU]
     "noReset" : True,
     "autoGrantPermissions": True,
     "unicodeKeyboard": True ,  # 启用 Unicode 键盘
     "resetKeyboard": True      # 重置软键盘状态
  }

driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)
driver.implicitly_wait(10)

#ini檔===========================================================================================================================================================================
config = configparser.ConfigParser()
current_dir = os.path.dirname(os.path.abspath(__file__))
config_keyfile = os.path.join(current_dir, 'IN DEV.ini')
config.read(config_keyfile, encoding='utf-8')
welcome = config.get('texts','welcome')
exit = config.get('texts','exit')
stay = config.get('texts','stay')  
maximum_text = config.get('texts','maximum_text')
advertising_amount = config.get('texts','advertising_amount')
get = config.get('texts','get')
phone_no = config.get('login','phone_no')
XPATH = config.get('basic','XPATH')

#DB配置=========================================================================================================================================================================
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

#B.1.登入頁========================================================================================================================================================================
print  ("\033[34;47mB.2.登入頁\033[m")
#Policy鏈結_檢查元素是否存在
driver.find_element(By.ID, packageid + "policyTextView").click()
print ("\033[32mPolicy鏈結 OK\033[0m")
time.sleep(5)
try:
    element1 = driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.webkit.WebView")
    correct_policypage = element1
    if correct_policypage:
        print("Privacy Policy_WebView \033[32mOK\033[0m")
    else:
        print("\033[91m" +"顯示錯誤"+ "\033[0m")
except Exception as e: # 若找不到元素或其他錯誤，可以在這裡處理
     print("\033[91m" +"未顯示錯誤訊息"+ "\033[0m", e)
time.sleep(2)

#scroll URL_Policy頁
driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.webkit.WebView").click()
x1, y1 = 348, 1436   # 起始位置
x2, y2 = 348, 213    # 終點位置
action = TouchAction(driver)
for _ in range(11):
 action.press(x=x1, y=y1).wait(1000).move_to(x=x2, y=y2).release().perform()
print ("\033[36mPolicy_scroll OK\033[0m") 
time.sleep(2)

#Policy_返回icon並且確定回到login
driver.find_element(By.ID, packageid + "toolBarBackTextView").click()
print ("\033[32m返回登入頁 OK\033[0m")
try: 
    login_element = driver.find_element(By.ID, packageid + "iconImageView")
    login = login_element
    if login:
        print("\033[33mlogin OK \033[0m")   
except Exception as e:
    # 若找不到元素或其他錯誤，可以在這裡處理
    print("\033[91m" +"未顯示錯誤訊息"+ "\033[0m", e)
time.sleep(2)

#============================================================================================================================================================================
####手機輸入欄位
driver.find_element(By.ID, packageid + "phoneEditText").send_keys(phone_no)
print("\033[32m輸入手機號 OK\033[0m")
time.sleep(2)
driver.find_element(By.ID, packageid +"sendOtpTextView").click()
print("\033[32m送出OTP OK\033[0m")
time.sleep(3)
driver.find_element(By.ID, packageid + "otpCodeEditText").send_keys('123456')
print("\033[32m輸入錯誤OTP OK\033[0m")
time.sleep(2)
driver.find_element(By.ID, packageid +"confirmTextView").click()
print("\033[32m登入confirm OK\033[0m")
time.sleep(2)
try:
    error_element = driver.find_element(By.XPATH, XPATH + "android.view.ViewGroup/android.widget.TextView[2][contains(@text, 'OTP code is wrong!')]")
    error_message = error_element.text
    if error_message:
        print("OTP code is wrong! \033[32mOK\033[0m")   
except Exception as e:
    # 若找不到元素或其他錯誤，可以在這裡處理
    print("\033[91m" +"未顯示錯誤訊息"+ "\033[0m", e)


driver.find_element(By.ID, packageid +"confirmTextView").click()
print("\033[32mOTP 彈窗confirm_close \033[0m")

driver.find_element(By.ID, packageid + "otpCodeEditText").send_keys("654321")
print("\033[32m輸入錯誤OTP OK\033[0m")

driver.find_element(By.ID, packageid +"confirmTextView").click()
print("\033[32m二次登入confirm OK\033[0m")
try:#連續輸入error message)
    error_element = driver.find_element(By.XPATH, XPATH + "android.view.ViewGroup/android.widget.TextView[2][contains(@text, 'Requests are too frequent, please try again in 10 seconds.')]")
    error_message = error_element.text
    if error_message:
        print("Requests are too frequent, please try again in 10 seconds. \033[32mOK\033[0m")
except Exception as e:
    # 若找不到元素或其他錯誤，可以在這裡處理
    print("\033[91m" +"未顯示錯誤訊息"+ "\033[0m", e)    
driver.find_element(By.ID, packageid +"confirmTextView").click()
print("\033[32mOTP 彈窗confirm_close \033[0m")

driver.find_element(By.ID, packageid +"otpCodeEditText").send_keys("00000") 
print("\033[32m重新輸入五碼OTP\033[0m")

driver.find_element(By.ID, packageid +"confirmTextView").click()
print("\033[31mOTP error彈窗confirm_close \033[0m")
try: #輸入錯誤(不足六碼)
    error_element = driver.find_element(By.ID, packageid + "otpErrorTextView")
    error_message = error_element.text 
    if error_message:
        print("Please double-check the code you received and try again. \033[32mOK\033[0m")
except Exception as e: # 若找不到元素或其他錯誤，可以在這裡處理
    print("\033[91m" +"未顯示錯誤訊息"+ "\033[0m", e)

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
        sql=f"SELECT content FROM hs_sms_record WHERE phone_no = '9999999999'ORDER BY id DESC LIMIT 1"
        cursor.execute(sql)
        result=cursor.fetchall()
time.sleep(2)       

# 提取数字部分
if result:
    message = result[0][0].strip()  # 提取短信内容
    match = re.search(r'\b\d+\b', message)
    
    if match:
        extracted_number = match.group()
        print ("\033[33m輸入錯誤手機號 9999999999 ", extracted_number)
else: 
     print("\033[31mOTP找不到OTP登入失敗。\033[0m")
time.sleep(5)
driver.find_element(By.ID, packageid + "otpCodeEditText").click()
print("\033[32m點擊OTP欄位 OK\033[0m")

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
        sql=f"SELECT content FROM hs_sms_record WHERE phone_no = '{phone_no}'ORDER BY id DESC LIMIT 1"
        cursor.execute(sql)
        result=cursor.fetchall()
time.sleep(2)
#提取正確OTP碼 
if result:
    message = result[0][0].strip()  # 提取短信内容
    match = re.search(r'\b\d+\b', message)
    
    if match:
        extracted_number = match.group()
        print ("\033[33m重新尋找正確OTP OK Extracted number:", extracted_number)
    else: 
     print("\033[31mOTP找不到OTP登入失敗。\033[0m")
time.sleep(2)

#輸入正確 OTP
driver.find_element(By.ID, packageid + "otpCodeEditText").send_keys(extracted_number)
print ("\033m[32m輸入正確OTP碼(手機號:9999999777) \033[0m")
time.sleep(2)

#點擊confirm
driver.find_element(By.ID, packageid +"confirmTextView").click()
print("\033[32m登入confirm OK\033[0m")
driver.quit()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




