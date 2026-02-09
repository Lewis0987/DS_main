from appium import webdriver
from selenium.webdriver.common.by import By
import time
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
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
packageid = config.get('basic','packageid')
exit = config.get('texts','exit')
stay = config.get('texts','stay')
welcome = config.get('texts','Welcome')
get = config.get('texts','get')
account = config.get('texts','account')
loan = config.get('texts','loan')
payment = config.get('texts','payment')
maximum_text = config.get("texts","maximum_text")
Privacy= config.get("texts","Privacy")
Disclosure = config.get("texts","Disclosure")



#A.1訪客首頁========================================================================================================================================================================
print  ("\033[34;47mA.1訪客首頁\033[m")
####歡迎語【welcome】
element = driver.find_element(By.ID, packageid + "titleTextView")
text1 = element.text
expected_text = welcome
if text1 == element.text:
    expected_text = f"{Fore.WHITE}{expected_text}{Style.RESET_ALL}" #INI加字色
    print("\033[32m歡迎語【welcome】OK\033[0m",expected_text)
else:
    print("\033[91m" +"welcome文字錯誤"+ "\033[0m")
time.sleep(2)

#看板【Maximum Loan Amount up to】
element = driver.find_element(By.ID, packageid + "amountTitleTextView")
text1 = element.text
expected_text = maximum_text
if text1 == element.text:
    expected_text = f"{Fore.WHITE}{expected_text}{Style.RESET_ALL}" #INI加字色
    print("\033[32m看板【Maximum Loan Amount up to】OK\033[0m",expected_text)
else:
    print("\033[91m" +"看板文字錯誤"+ "\033[0m")
time.sleep(2)

#廣告額度【₹ 80,000】
element = driver.find_element(By.ID, packageid + "amountTextView")
text1 = element.text
expected_text = maximum_text
if text1 == element.text:
    expected_text = f"{Fore.WHITE}{expected_text}{Style.RESET_ALL}" #INI加字色
    print("\033[32m廣告額度【₹ 80,000】OK\033[0m",expected_text)
else:
    print("\033[91m" +"廣告額度文字錯誤"+ "\033[0m")
time.sleep(2)

#### Exit_alart_exit
driver.press_keycode(4) #離開APP彈窗
element = driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.TextView[2]")
text1 = element.text
expected_text= exit 
if text1 == expected_text:
    expected_text = f"{Fore.YELLOW}{expected_text}{Style.RESET_ALL}"
    print("\033[32mExit_彈窗實現\033[0m",expected_text)
else:
    print("\033[91m" +"彈窗失敗"+ "\033[0m")
time.sleep(2)
#離開彈窗[Leave]按鈕
driver.find_element(By.ID, "com.ind.kyc.application:id/negativeTextView").click()
print ("\033[32mLeave OK\033[0m")

#卓面回APP
driver.find_element(By.XPATH, "//android.widget.TextView[@content-desc='Stream IND']").click() 
print ("\033[32m桌面回APP OK\033[0m")
time.sleep(5)

#### Exit_alart_stay
driver.press_keycode(4)
element = driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.TextView[3]")
text1 = element.text
expected_text = stay
if text1 == expected_text:
    expected_text = f"{Fore.YELLOW}{expected_text}{Style.RESET_ALL}"
    print("\033[32mExit_彈窗實現\033[0m",expected_text)
else:
    print("\033[91m" +"彈窗失敗"+ "\033[0m")
time.sleep(2)
#離開彈窗[Stay on this page]按鈕
driver.find_element(By.ID, "com.ind.kyc.application:id/positiveTextView").click()
print ("\033[32mStay on this page OK\033[0m")
time.sleep(2)

####訪客首頁Get my limit
element = driver.find_element(By.ID, "com.ind.kyc.application:id/nextTextView") 
text1 = element.text
expected = get
if text1 == expected:
    expected  = f"{Fore.WHITE}{expected}{Style.RESET_ALL}"
    print("\033[32mGet my limit OK\033[0m",expected)
else:
    print("\033[91m" +"文字錯誤"+ "\033[0m")
#執行[Get my limit]按鈕
driver.find_element(By.ID, packageid +"nextTextView").click() 
print ("\033[32m點擊Get my limit OK\033[0m")
time.sleep(2)
try:
    backicon_login_element = driver.find_element(By.ID, packageid + "ivPreviousPage").click()
    login = backicon_login_element
    if login:
        print("\033[33m返回訪客 OK \033[0m")   
except Exception as e:
    # 若找不到元素或其他錯誤，可以在這裡處理
    print("\033[91m" +"未顯示錯誤訊息"+ "\033[0m", e)
time.sleep(2)

####訪客首頁_導航條account
element = driver.find_element(By.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.widget.LinearLayout[3]/android.view.ViewGroup/android.widget.TextView")
account = element.text
expected = account
if account == expected:
   print("\033[32maccount text OK\033[0m",expected) 
else:
    print("\033[91m" +"文字錯誤"+ "\033[0m")

#執行[account]導航條
driver.find_element(By.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.widget.LinearLayout[3]/android.view.ViewGroup/android.widget.TextView").click()
print ("\033[32m導航條_點擊account OK\033[0m")
time.sleep(3)

# 【尚未登入】/ account頁_[Privacy Policy]text
element = driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView")
Privacy_text = element.text
expected = Privacy
if Privacy_text == expected:
   print("\033[32m[Privacy Policy]text OK\033[0m",expected) 
else:
    print("\033[91m" +"文字錯誤"+ "\033[0m")

#【尚未登入】/account頁_[Privacy Policy]選項跳轉
element = driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView").click()
Privacy = element
expected = Privacy
if Privacy == expected:
   print("\033[32m[Privacy Policy]選項跳轉 OK\033[0m") 
else:
    print("\033[91m" +"跳轉失敗"+ "\033[0m")
time.sleep(5)

#scroll URL_Policy頁
driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.webkit.WebView").click()
x1, y1 = 348, 1436   # 起始位置
x2, y2 = 348, 213    # 終點位置
action = TouchAction(driver)
for _ in range(12):
 action.press(x=x1, y=y1).wait(1000).move_to(x=x2, y=y2).release().perform()
print ("\033[36mPolicy_scroll OK\033[0m") 
time.sleep(2)

#Policy_返回icon並且確定回到account頁
driver.find_element(By.ID, packageid + "toolBarBackTextView").click()
print ("\033[32m點擊icon返回上一頁 OK\033[0m")
time.sleep(2)
try:
    back_element = driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup")
    print("\033[32m返回到account OK \033[0m")   
except Exception as e:
    # 若找不到元素或其他錯誤，可以在這裡處理
    print("\033[91m" +"【找不到元素其他錯誤訊息】"+ "\033[0m", e)

# 【尚未登入】/ account頁_[Disclosure statement]text
element = driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView")
Disclosure_text = element.text
expected = Disclosure
if Disclosure_text == expected:
   print("\033[32m[Disclosure statement]text OK\033[0m",expected) 
else:
    print("\033[91m" +"文字錯誤"+ "\033[0m")

#【尚未登入】/account頁_[Disclosure statement]選項跳轉
element = driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView").click()
Disclosure = element
expected = Disclosure
if Disclosure == expected:
   print("\033[32m[Disclosure statement]選項跳轉 OK\033[0m") 
else:
    print("\033[91m" +"跳轉失敗"+ "\033[0m")
time.sleep(5)

#scroll URL_Disclosure頁
driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.webkit.WebView/android.webkit.WebView").click()
x1, y1 = 348, 1436   # 起始位置
x2, y2 = 348, 213    # 終點位置
action = TouchAction(driver)
for _ in range(4):
 action.press(x=x1, y=y1).wait(1000).move_to(x=x2, y=y2).release().perform()
print ("\033[36mDisclosure_scroll OK\033[0m") 
time.sleep(2)

#Disclosure_返回icon並且確定回到account頁
driver.find_element(By.ID, packageid + "toolBarBackTextView").click()
print ("\033[32m點擊icon返回上一頁 OK\033[0m")
time.sleep(2)
try:
    back_element = driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup")
    print("\033[32m返回到account OK \033[0m")   
except Exception as e:
    # 若找不到元素或其他錯誤，可以在這裡處理
    print("\033[91m" +"【找不到元素其他錯誤訊息】"+ "\033[0m", e)

####訪客首頁_導航條Loan
element = driver.find_element(By.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.view.ViewGroup/android.widget.TextView")
loan = element.text
expected = loan
if loan == expected:
   print("\033[32mloan text OK\033[0m",expected) 
else:
    print("\033[91m" +"文字錯誤"+ "\033[0m")
#執行[loan]導航條
driver.find_element(By.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.view.ViewGroup/android.widget.TextView").click()
print ("\033[32m導航條_點擊loan OK\033[0m")
time.sleep(5)

####訪客首頁_導航條payment
element = driver.find_element(By.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.view.ViewGroup/android.widget.TextView")
payment = element.text
expected = payment
if payment == expected:
   print("\033[32mpayment text OK\033[0m",expected) 
else:
    print("\033[91m" +"文字錯誤"+ "\033[0m")
time.sleep(2)

#執行[payment]導航條
driver.find_element(By.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.view.ViewGroup/android.widget.TextView").click()
print ("\033[32m導航條_點擊payment OK\033[0m")
time.sleep(3)
try:
    back_element = driver.find_element(By.ID, packageid + "ivPreviousPage")
    print("\033[32m返回icon OK \033[0m")   
except Exception as e:
    # 若找不到元素或其他錯誤，可以在這裡處理
    print("\033[91m" +"未顯示錯誤訊息"+ "\033[0m", e)
#執行登入頁[<]icon
driver.find_element(By.ID, packageid + "ivPreviousPage").click()
print("\033[35m登入頁點擊[<]icon OK \033[0m")
time.sleep(2)

#返回訪客首頁
try:
    back_element = driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout")
    print("\033[32m回到訪客首頁 OK \033[0m")   
except Exception as e:
    # 若找不到元素或其他錯誤，可以在這裡處理
    print("\033[91m" +"未顯示錯誤訊息"+ "\033[0m", e)
time.sleep(2)

