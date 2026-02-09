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
config = configparser.ConfigParser()
current_dir = os.path.dirname(os.path.abspath(__file__))
config_keyfile = os.path.join(current_dir, 'IN DEV.ini')
config.read(config_keyfile, encoding='utf-8')
packageid=config.get('basic','packageid')
XPATH = config.get('basic','XPATH')
stay = config.get('texts','stay')
policy = config.get('login','policy')

print  ("\033[34;47mA.2.登入頁\033[m")

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

#scoll_Policy頁
driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.webkit.WebView").click()
x1, y1 = 348, 1436   # 起始位置
x2, y2 = 348, 213    # 終點位置
action = TouchAction(driver)
for _ in range(11):
 action.press(x=x1, y=y1).wait(1000).move_to(x=x2, y=y2).release().perform()
print ("\033[36mPolicy_scroll OK\033[0m") 
time.sleep(2)

#Policy_返回icon
driver.find_element(By.ID, packageid + "toolBarBackTextView").click()
print ("\033[32m返回登入頁 OK\033[0m")
time.sleep(2)

#login頁
try:
    login_element = driver.find_element(By.ID, packageid + "iconImageView")
    login = login_element
    if login:
        print("\033[33mlogin OK \033[0m")   
except Exception as e:
    # 若找不到元素或其他錯誤，可以在這裡處理
    print("\033[91m" +"未顯示錯誤訊息"+ "\033[0m", e)
time.sleep(2)



