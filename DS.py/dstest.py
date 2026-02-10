from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import( 
TimeoutException, ElementClickInterceptedException, ElementNotInteractableException, NoSuchElementException, NoSuchWindowException,StaleElementReferenceException)
from pathlib import Path
from colorama import Fore,Style
import os, time
import sys
import threading
import configparser
import pyperclip
import re

# ====== 設定下載路徑 ====== 
download_path =r"C:\Users\User\Downloads"  #另種寫法 "C:\\Users\howar\Downloads" 
#r"D:\下載"	✅ 推薦	不用擔心 \ 變跳脫符號
#"D:\\下載"	✅ 推薦	手動雙斜線跳脫更安全
#"D:\下載"	❌ 不推薦	萬一剛好有 \t、\n、\r 很容易踩坑
# 【設定 ChromeOptions】 
# ====== 初始化 Chrome Driver ======
options = webdriver.ChromeOptions()
chrome_options = Options()
chrome_options.add_argument("--log-level=3")  # 只顯示 fatal 錯誤
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # 關閉 GCM 日誌
# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
config_keyfile = os.path.join(current_dir, 'IND.ini')
# 讀取配置文件
config = configparser.ConfigParser()
config.read(config_keyfile, encoding='utf-8')

################確認遊戲模板(請輸入 'U1、U2.../V1、V2...')###########################
version = 'IN'
ui_numbers = ['INPV6']
################確認帳號#######################################
phone='8888888888' #for 登入
# 初始化Chrome浏览器
driver = webdriver.Chrome(service=Service(), options=chrome_options)
# 開啟網页並將模板引入
WebDriverWait(driver, 10)
for product in ui_numbers:
    url = config.get(version, product)
    driver.get(url)
    driver.maximize_window() #網頁整頁

#<<<<<<<<<<<<<<<<<<<<<背景偵測popup，並關閉>>>>>>>>>>>>>>>>>>>>>>
exit_event = threading.Event()
def handle_popups(driver):
    print("👀 handle_popups 背景監聽啟動")
    while not exit_event.is_set():
        try:
            # 在这里执行查找弹窗的操作
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//img[contains(@alt, 'first_recharge_popup')]")))
            
            # 找到弹窗后执行关闭的操作
            close_button = driver.find_element(By.CSS_SELECTOR, '[alt="ic_close"]')
            ActionChains(driver).move_to_element(close_button).click().perform()                                  
        except (TimeoutException, StaleElementReferenceException):
            # 超时异常，表示未找到弹窗，不输出错误信息
            pass
        except (NoSuchWindowException, StaleElementReferenceException):
            # 窗口已經被關閉，結束循環
            break
        time.sleep(0.5)  # 建議加這行，減少 CPU 負擔
#<<<<<<<<<<<<<<<<<<<<<背景偵測popup，並關閉>>>>>>>>>>>>>>>>>>>>>>
# 主程式中呼叫
#<<<<<<<<<<<<<<<<<<<<<背景偵測popup，開始>>>>>>>>>>>>>>>>>>>>>>
popup_thread = threading.Thread(target=handle_popups, args=(driver,), daemon=True) #✅ 正確取得 thread 實體並啟動
popup_thread.start()
print('\033[35m⭐️⭐️背景偵測popup，開始 ⭐️⭐️\033[0m')
#<<<<<<<<<<<<<<<<<<<<<背景偵測popup，開始>>>>>>>>>>>>>>>>>>>>>>

sleep(1)
#-------------------------1.A.首頁模塊 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# A.首頁 Popup 
    # 首頁[Subscribe] 訂閱 
print('\033[33m首頁[Subscribe] 訂閱 \033[0m')
print("\033[44m\033[32m" + "Subscribe 訂閱" + "\033[0m")
try:
    Subscribe =  WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Later')]"))
    ).click()
    print('A-1.Subscribe_Later \033[32mOK\033[0m')
except TimeoutException:
    print("\033[94m未偵測活動元素，繼續流程...\033[0m")


'''#首頁[surprise_reward_popup] 【1】>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
print("\033[107m\033[30m" + "A.[首頁/popup]" + "\033[0m")
popup = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.XPATH, "//img[contains(@alt, 'popup_surprise_reward')]"))
).click()
print('A-1.surprise_reward popup \033[32mOK\033[0m')
try:
    popup = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'The reward has been claimed')]"))
    )
    print('A-1.已領取過獎勵toast \033[32mOK\033[0m')
        # 領取過獎勵重整網頁
    driver.refresh()
    sleep(3)
    try:
        popup = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//img[contains(@alt, 'first_recharge_popup')]"))
        )
        print("A-1-1.點擊首充 popup \033[32mOK\033[0m")
         # 找到關閉按鈕並點擊
        close_btn = driver.find_element(By.XPATH, "//img[@alt='ic_close']").click()
        print("A-1-1.【關閉】首充 popup \033[32mOK\033[0m")
    except TimeoutException:
        print("\033[93mA-1-1.未偵測到 ，可略過。\033[0m")
except TimeoutException:
        print("\033[93m" + "A-1.未偵測到已領取文字，繼續流程..." + "\033[0m")
'''

    #首頁[充值大輪盤_popup]【A】
print('\033[33m充值大輪盤【A】\033[0m')
print("\033[44m\033[32m" + "充值大輪盤【A】" + "\033[0m")
try:
    popup = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'SPIN')]"))
    )
    print('A.Prize wheel_popup \033[32mOK\033[0m')
    
    sleep(1)
    try:
        popup = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, "//img[contains(@alt, 'first_recharge_popup')]"))
        )
        print("A-1-1.點擊首充 popup \033[32mOK\033[0m")
         
        close_btn = driver.find_element(By.XPATH, "//img[@alt='ic_close']").click()  # 找到關閉按鈕並點擊
        print("A-1-1.【關閉】首充 popup \033[32mOK\033[0m")
    except TimeoutException:
        print("\033[94m模擬內彈.未偵測到 ，可略過。\033[0m")
    
    close_btn = driver.find_element(By.XPATH, "//img[@alt='ic_close']").click()
    print("A-1-1.【關閉】首充 popup \033[32mOK\033[0m")
except TimeoutException:
        print("\033[94m" + "A-1.未偵測活動元素，繼續流程..." + "\033[0m")

sleep(0.5)
    #首頁[首充_popup]【2】
print('\033[33m首充Popup\033[0m')
print("\033[44m\033[32m" + "首充Popup" + "\033[0m")
try:
    popup = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "//img[contains(@alt, 'popup_first_recharge_vb')]"))
    )
    print('A-2.FirstRecharge_popup \033[32mOK\033[0m')
    
    sleep(1)
    try:
        popup = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, "//img[contains(@alt, 'first_recharge_popup')]"))
        )
        print("A-1-1.首充 popup \033[32mOK\033[0m")
         # 找到關閉按鈕並點擊
        close_btn = driver.find_element(By.XPATH, "//img[@alt='ic_close']").click()
        print("A-1-1.【關閉】首充 popup \033[32mOK\033[0m")
    except TimeoutException:
        print("\033[94m模擬內彈.未偵測到 ，可略過。\033[0m")
    
    close_btn = driver.find_element(By.XPATH, "//img[@alt='ic_close']").click()
    print("A-1-1.【關閉】首充 popup \033[32mOK\033[0m")
except TimeoutException:
        print("\033[94m" + "A-1.未偵測活動元素，繼續流程..." + "\033[0m")

sleep(0.5)
    #首頁[mission_popup]【3】>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
print('\033[33mmission 任務中心 \033[0m')
print("\033[44m\033[32m" + "mission 任務中心" + "\033[0m")
try:
    popup = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'p-4 box-border')]"))
    )
    print('A-3.mission_popup \033[32mOK\033[0m')

    sleep(1)
    try:
        popup = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, "//img[contains(@alt, 'first_recharge_popup')]"))
        )
        print("A-1-1.點擊首充 popup \033[32mOK\033[0m")
         # 找到關閉按鈕並點擊
        close_btn = driver.find_element(By.XPATH, "//img[@alt='ic_close']").click()
        print("A-1-1.【關閉】首充 popup \033[32mOK\033[0m")
    except TimeoutException:
        print("\033[94m模擬內彈.未偵測到 ，可略過。\033[0m")

    close_btn = driver.find_element(By.XPATH, "//img[@alt='ic_close']").click()
    print("A-3.【關閉】mission popup \033[32mOK\033[0m")
except TimeoutException:
        print("\033[94m" + "A-1.未偵測活動元素，繼續流程..." + "\033[0m")

sleep(0.5)
    #首頁[club_popup]【4】>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
print('\033[33mclub 俱樂部 \033[0m')
print("\033[44m\033[32m" + "club 俱樂部" + "\033[0m")

try:
    popup = WebDriverWait(driver, 1).until(
    EC.presence_of_element_located((By.XPATH, "//img[contains(@alt, 'popup_club')]"))
    )
    print('A-4.club popup \033[32mOK\033[0m') 
    sleep(1)
    try:
        popup = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "//img[contains(@alt, 'first_recharge_popup')]"))
        )
        print("A-1-1.點擊首充 popup \033[32mOK\033[0m")
         # 找到關閉按鈕並點擊
        close_btn = driver.find_element(By.XPATH, "//img[@alt='ic_close']").click()
        print("A-1-1.【關閉】首充 popup \033[32mOK\033[0m")
    except TimeoutException:
        print("\033[94m模擬內彈.未偵測到 ，可略過。\033[0m")
        
    close_btn = driver.find_element(By.XPATH, "//img[@alt='ic_close']").click()
    print("A-4.【關閉】popup_club \033[32mOK\033[0m")
except TimeoutException:
        print("\033[94m" + "A-4.未偵測活動元素，繼續流程..." + "\033[0m")


sleep(1)
    #首頁[telegram_popup]【5】>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
print('\033[33mclub telegram gift\033[0m')
print("\033[44m\033[32m" + "telegram gift" + "\033[0m")
try:
    popup = WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.XPATH, "//img[contains(@alt, 'popup_subscribe_telegram')]"))
)
    print('A-5.telegram popup \033[32mOK\033[0m')
    sleep(1)
    try:
        popup = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "//img[contains(@alt, 'first_recharge_popup')]"))
        )
        print("A-1-1.點擊首充 popup \033[32mOK\033[0m")
         # 找到關閉按鈕並點擊
        close_btn = driver.find_element(By.XPATH, "//img[@alt='ic_close']").click()
        print("A-1-1.【關閉】首充 popup \033[32mOK\033[0m")
    except TimeoutException:
        print("\033[94m模擬內彈.未偵測到 ，可略過。\033[0m")
   
   # 找到關閉按鈕並點擊
    close_btn = driver.find_element(By.XPATH, "//img[@alt='ic_close']").click()
    print("A-5.關閉telegram popup \033[32mOK\033[0m")
except TimeoutException as e:
    print("\033[94m" + "A-5.未偵測活動元素，繼續流程..." + "\033[0m")
    checked = True  # 防止重複執行
except Exception as e:
    print("\033[91mA-5 其他錯誤：\033[0m", str(e).split("Stacktrace")[0])   # 只保留 Stacktrace 前的部分
    checked = True  # 防止重複執行


sleep(1)
    #首頁[Jackpot_popup]【6】>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
print('\033[33mJackpot \033[0m')
print("\033[44m\033[32m" + "Jackpot" + "\033[0m")
try:
    popup = WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.XPATH, "//img[contains(@alt, 'popup_jackpot')]"))
)
    print('A-6.jackpot popup \033[32mOK\033[0m')
    sleep(1)
    try:
        popup = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "//img[contains(@alt, 'first_recharge_popup')]"))
        )
        print("A-1-1.點擊首充 popup \033[32mOK\033[0m")
         # 找到關閉按鈕並點擊
        close_btn = driver.find_element(By.XPATH, "//img[@alt='ic_close']").click()
        print("A-1-1.【關閉】首充 popup \033[32mOK\033[0m")
    except TimeoutException:
        print("\033[94m模擬內彈.未偵測到 ，可略過。\033[0m")
   
    # 找到關閉按鈕並點擊
    close_btn = driver.find_element(By.XPATH, "//img[@alt='ic_close']").click()
    print("A-6.關閉jackpot popup \033[32mOK\033[0m")
    
except TimeoutException as e:
    print("\033[94m" + "A-6.未偵測活動元素，繼續流程..." + "\033[0m")
    checked = True  # 防止重複執行
except Exception as e:
    print("\033[91mA-6 其他錯誤：\033[0m", str(e).split("Stacktrace")[0])  # 只保留 Stacktrace 前的部分
    checked = True  # 防止重複執行


sleep(1)
try:  
    # B.2-1 首頁【Banner】廣告模塊 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    print('\033[33mB.2-1 首頁【Banner】\033[0m')
    print("\033[44m\033[32m" + "B.2-1 首頁【Banner】廣告模塊" + "\033[0m")
    sleep(0.5)
    #尋找首頁Banner參數【'0_ENTER_GAME', '1_TEAM_CLUB', '2_FIRST_CHARGE', '3_CHARGE_WHEEL', '4_INVITE_WHEEL','5_RANKINGS', '6_GIFT_CODE', '7_VIP', '8_PIGGY_BANK', '9_Daily Mission'】
    banner_alts = ['0_ENTER_GAME', '1_TEAM_CLUB', '2_FIRST_CHARGE', '3_CHARGE_WHEEL', '4_INVITE_WHEEL','5_RANKINGS', '6_GIFT_CODE', '7_VIP', '8_PIGGY_BANK', '9_Daily Mission']
    clicked_banners = set()  # 記錄哪些 banner 成功點擊過
    clicked_banners.clear()  # 僅針對已存在的集合清空

    # 決定要用哪一組名稱對照表 ，如果沒有參數 => 未定義
    if ui_numbers == ['INV6']:
        banner_alts = ['0_ENTER_GAME', '1_TEAM_CLUB', '2_FIRST_CHARGE', '3_CHARGE_WHEEL', '4_INVITE_WHEEL','5_RANKINGS', '6_GIFT_CODE', '7_VIP', '8_PIGGY_BANK', '9_Daily Mission']
        alt_names = { 
        '0_ENTER_GAME': '✈️ 飛機遊戲',
        '1_TEAM_CLUB': '👥 團隊俱樂部',
        '2_FIRST_CHARGE': '💎 首儲活動',
        '3_CHARGE_WHEEL': '🎡 充值轉盤',
        '4_INVITE_WHEEL': '🎯 邀請轉盤',
        '5_RANKINGS': '🏆 排行榜',
        '6_GIFT_CODE': '🎁 禮包碼',
        '7_VIP': '👑 VIP專區',
        '8_PIGGY_BANK': '🐷 虧損反水', 
        '00_Daily Mission': '📋 任務中心'   
    } 
    else:
        banner_alts = ['0_FIRST_CHARGE', '1_PIGGY_BANK', '2_ENTER_GAME', '3_TEAM_CLUB', '4_CHARGE_WHEEL','5_INVITE_WHEEL', '6_GIFT_CODE', '7_VIP', '8_PIGGY_BANK']
        alt_names = { 
        '0_FIRST_CHARGE': '💎 首儲活動',
        '1_PIGGY_BANK': '🐷 虧損反水',
        '2_ENTER_GAME': '✈️ 飛機遊戲',
        '3_TEAM_CLUB': '👥 團隊俱樂部',
        '4_CHARGE_WHEEL': '🎡 充值轉盤',
        '5_INVITE_WHEEL': '🎯 邀請轉盤',
        '6_GIFT_CODE': '🎁 禮包碼',
        '7_VIP': '👑 VIP專區',
        '8_BANK_BANK': '模擬無元素'
    }
    
    running = True  # 控制 while 是否繼續
    error_reported = False   # ⬅️ 新增旗標，避免重複印
    while running: 
        for alt_text in banner_alts:
            print(f"\n👉 正在處理 Banner: {alt_text}")
            if alt_text in clicked_banners:
                continue  # 如果已經點過這個廣告就跳過
            try:
                banner = WebDriverWait(driver, 60).until(
                 EC.element_to_be_clickable((By.XPATH, f"//img[contains(@alt, '{alt_text}')]"))
                )
                if banner.is_displayed():
                    banner.click()
                    print(f" 點擊廣告成功【{alt_text}】\033[32mOK\033[0m")
                    print(f"✅ \033[33m【{alt_names.get(alt_text, alt_text)}】\033[32m\033[0m")
                    # ...其餘流程                
                    time.sleep(1)
                    # ========================================
                                        # ====== ⛔ 錯誤訊息偵測區段（下架訊息）======
                    try:
                        WebDriverWait(driver, 3).until(
                            EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "This game has been taken down")]'))
                        )
                        print(f"\033[31m⚠️【{alt_text}】遊戲異常略過返回首頁。\033[0m")
                        clicked_banners.add(alt_text)
                        continue
                    except TimeoutException:
                        pass # 沒跳出錯誤 → 正常流程

                                        # ====== 💰 出現 Collect 按鈕時，自動點擊 ======
                    try:
                        collect_btn = WebDriverWait(driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Collect')]"))
                        )
                        collect_btn.click()
                        print(f"\033[33m💰 Collect 按鈕，已點擊成功。\033[0m")
                        time.sleep(1)
                        clicked_banners.add(alt_text)
                        continue
                    except TimeoutException:
                        pass  # 沒有 Collect 按鈕就略過
                    # ========================================

                    driver.back()  # 回首頁
                    print("離開返回首頁 \033[32mOK\033[0m")
                    time.sleep(1)
                    clicked_banners.add(alt_text) #繼續點擊 banner
            except NoSuchElementException:
                pass
            except Exception as e:
                if "invalid session id" in str(e):
                    if not error_reported:   # ⬅️ 只在第一次觸發時印
                        print("⚠️ Driver session 已失效，程式即將結束。")
                        error_reported = True
                    running = False   # ⬅️ 停止 while
                else:
                    print(f"\033[31m❌ 例外或不再架上【{alt_names.get(alt_text, alt_text)}】，直接跳過\033[0m")
                    continue   # 直接跳下一個 Banner
            else:
                print("沒有錯誤，成功執行！")
            # 👉 跑完一輪就結束
        print("\033[33m🎉 所有 Banners 已處理完畢，程式結束！\033[0m") 
        break # 如果 都點過了，就結束
    # ======= 完成檢查 =======
    missing = set(banner_alts) - clicked_banners 
    total = len(banner_alts)   # 這是所有 Banner 的清單
    if missing:
        print(f"\033[31m⚠️ 還有 {len(missing)}/{total} 個 Banner 沒被觸發: {missing}\033[0m")
    else:
        print(f"\033[32m🎉 所有 Banner 都已觸發完成！總數 {total}\033[0m")
        time.sleep(1)

    sleep(1)
    # B.2-1 首頁【Banner】廣告模塊 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>





#<<<<<<<<<<<<<<<<<<<<<背景偵測popup，結束>>>>>>>>>>>>>>>>>>>>>>
except TimeoutException:
    pass
finally:
    print('\033[35m⭐️⭐️handle_popups 背景監聽結束 ⭐️⭐️\033[0m')
    exit_event.set()
    popup_thread.join()
#<<<<<<<<<<<<<<<<<<<<<背景偵測popup，結束>>>>>>>>>>>>>>>>>>>>>>








input('Press Enter to exit...')

