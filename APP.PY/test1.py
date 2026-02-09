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
     "resetKeyboard": True   # 重置软键盘状态
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
welcome = config.get('texts','welcome')
get = config.get('texts','get')
packageid = config.get('basic','packageid')
phone_no= config.get('login','phone_no')

driver.find_element(By.ID, packageid + "phoneEditText").send_keys(phone_no)
print("\033[32m輸入手機號 OK\033[0m")
time.sleep(2)

driver.find_element (By.ID, packageid +"sendOtpTextView").click()
print("\033[32m送出OTP OK\033[0m")
time.sleep(2)

driver.find_element(By.ID, packageid +"otpCodeEditText").send_keys("00000") 
print("\033[32m重新輸入五碼OTP\033[0m")
time.sleep(2)

driver.find_element(By.ID, packageid +"confirmTextView").click()
print("\033[31mOTP confirm_error_message \033[0m")
time.sleep(2)

driver.find_element(By.ID, packageid + "otpErrorTextView") 
try:
    error_element = driver.find_element(By.ID, packageid + "otpErrorTextView")
    error_message = error_element.text 
    if "*Please double-check the code you received and try again." in error_message: 
        print("\033[32m登入confirm_輸入不足6碼錯誤\033[0m" + '*Please double-check the code you received and try again.')   
except Exception as e: # 若找不到元素或其他錯誤，可以在這裡處理
    print("\033[91m" +"未顯示錯誤訊息"+ "\033[0m", e)

driver.quit()





