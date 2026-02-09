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

#C.1.使用者首頁========================================================================================================================================================================
print  ("\033[34;47mC.1.未認證使用者首頁\033[0m")
#C.1-1未認證跑馬燈(檢查元素)
driver.find_element (By.ID, packageid + "btnMarquee")
print ("\033[32mC.1-1 未認證首頁_跑馬燈 OK\033[0m")
#檢查跑馬燈文案
element = driver.find_element (By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.widget.LinearLayout/android.view.ViewGroup[1]/android.widget.Button")
marquee = element.text
#檢查相對文案內容
expected_text = 'Borrow now for discounts, get certified immediately to earn the discounts.'
#檢查事件文案內容並印出訊息
if marquee == expected_text:
   expected_text = f"{Fore.WHITE}{expected_text}{Style.RESET_ALL}"
   print("\033[32mC.1-1【實現跑馬燈】OK \033[0m",expected_text) 
else:
    print("\033[91m" +"C.1-1跑馬燈文字錯誤"+ "\033[0m") 
time.sleep(2)

#C.1-2 未認證客服功能icon
driver.find_element(By.ID, packageid +"sivRightIcon")
print("\033[32mC.1-2未認證首頁_客服icon OK \033m")
#提交客服icon，確認跳轉【Customer Service】
driver.find_element(By.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.ScrollView/android.widget.LinearLayout/android.view.ViewGroup[2]/android.widget.ImageView").click()
print("\033[32m1-2未認證首頁_提交客服icon OK \033m")
time.sleep(2)
try:
        element = driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup")
        # 如果找到了元素，可以输出错误信息或执行其他操作
        print("\033[33m1-2 跳轉【Customer Service】 \033[0m"+"\033[32mOK\033[0m" )         
except NoSuchElementException:
        # 如果捕获到 NoSuchElementException 异常，说明元素也不存在，一切正常
        print("\033[91m" +"1-2跳轉錯誤"+ "\033[0m")
time.sleep(2)
#返回icon【Customer Service】
driver.find_element(By.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.ImageButton").click()
