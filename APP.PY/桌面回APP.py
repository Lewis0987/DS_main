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
config_keyfile = os.path.join(current_dir, 'DB資料.ini')
config.read(config_keyfile, encoding='utf-8')
exit = config.get('texts','exit')
stay = config.get('texts','stay')
welcome = config.get('texts','welcome')

####訪客首頁
element = driver.find_element(By.ID, "com.ind.kyc.application:id/titleTextView") 
text1 = element.text

expected_text = welcome

if text1 == expected_text:
    expected_text = f"{Fore.WHITE}{expected_text}{Style.RESET_ALL}"
    print("\033[32mwelcome OK\033[0m",expected_text)
else:
    print("\033[91m" +"welcome文字錯誤"+ "\033[0m")


