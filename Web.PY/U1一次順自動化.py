from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import os
import configparser
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException 
from selenium.common.exceptions import TimeoutException, NoSuchWindowException
import time
import sys
import threading
#<<<<<<<<<<<<<<<<<<<<<背景偵測popup，並關閉>>>>>>>>>>>>>>>>>>>>>>
exit_event = threading.Event()
def handle_popups(driver):
    while not exit_event.is_set():
        try:
            # 在这里执行查找弹窗的操作
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Equilíbrio insuficiente!") or contains(text(), "Convide usuários limitados para compartilhar")]')))
            # 找到弹窗后执行关闭的操作
            close_button = driver.find_element(By.CSS_SELECTOR, '[alt="Close Icon"]')
            ActionChains(driver).move_to_element(close_button).click().perform()
        except TimeoutException:
            # 超时异常，表示未找到弹窗，不输出错误信息
            pass
        except NoSuchWindowException:
            # 窗口已經被關閉，結束循環
            break
#<<<<<<<<<<<<<<<<<<<<<背景偵測popup，並關閉>>>>>>>>>>>>>>>>>>>>>>
###VVVVVVVVVVV計算print出的錯誤率VVVVVVVVVVVVVVVVV##############
class ColorPrintCounter:
    def __init__(self):
        self.total_count = 0
        self.red_count = 0
        self.green_count = 0

    def write(self, text):
        sys.__stdout__.write(text)
        color_codes = ["\033[32m", "\033[91m"]
        for color_code in color_codes:
            if color_code in text:
                self.total_count += 1
                if color_code == "\033[32m":
                    self.green_count += 1
                elif color_code == "\033[91m":
                    self.red_count += 1

    def flush(self):
        sys.__stdout__.flush()
    def reset_counts(self):
        self.total_count = 0
        self.red_count = 0
        self.green_count = 0
sys.stdout = ColorPrintCounter()
###^^^^^^^^^^^^計算print出的錯誤率^^^^^^^^^^^^^^^^^^#############
config = configparser.ConfigParser()
# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
config_keyfile = os.path.join(current_dir, 'game.ini')
# 讀取配置文件
config.read(config_keyfile, encoding='utf-8')
################確認遊戲模板(請輸入 'U1、U2.../V1、V2...')###########################
ui_version = 'U1'
product_numbers = ['V37'] #跑多產品['xx','xx','xx']

def main():
    driver = webdriver.Chrome()

    for product in product_numbers:
        url = config.get(ui_version, product)
        sys.stdout.reset_counts()

        # 打开网页
        driver.get(url)
        WebDriverWait(driver, 10)
        driver.maximize_window()

        
#-------------------------1.登入模塊
        print("\033[107m\033[30m" + "1.登入模塊" + "\033[0m")
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[type="number"]'))
            ).send_keys('9999999888')
        element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[type="password"]'))
            ).send_keys('1111')
        sleep(0.5)
        button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "ConfirmButton")]'))
            ).click()
            # 尋找彈窗元素判斷是否登入
        try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Convide usuários limitados para compartilhar")]'))
                )
                # 如果找到了元素，表示登录成功
                print("1. 登入成功\033[32mOK\033[0m")
                
        except TimeoutException:
                # 如果超时，表示登录失败
                print("\033[91m" +"1. 登录失败_檢查手機號註冊"+ "\033[0m")
            #-------------------------2.popup模塊
        print("\033[107m\033[30m" + "2.popup模塊" + "\033[0m")
        try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Convide usuários limitados para compartilhar")]'))
                )
                print("2.1 邀請popup顯示\033[32mOK\033[0m")
        except TimeoutException:
                print("\033[91m" +"2.1 邀請popup未顯示"+ "\033[0m")
        sleep(0.5)
        element=WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'[alt="Close Icon"]'))
            ).click()
        try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Equilíbrio insuficiente!")]'))
                )
                print("2.2 充值popup顯示\033[32mOK\033[0m")
        except TimeoutException:
                print("\033[91m" +"2.2 充值popup不顯示"+ "\033[0m")
        sleep(0.5)
        element=WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'[alt="Close Icon"]'))
                ).click()
        print("\033[43m\033[30m" + "HEADER模塊" + "\033[0m")
    #<<<<<<<<<<<<<<<<<<<<<背景偵測popup，開始>>>>>>>>>>>>>>>>>>>>>>
        popup_thread = threading.Thread(target=handle_popups, args=(driver,))
        popup_thread.start()
    #<<<<<<<<<<<<<<<<<<<<<背景偵測popup，開始>>>>>>>>>>>>>>>>>>>>>>
        try:    
            #-------------------------3.HEADER-Jogos模塊
            sleep(0.5)
            print("\033[107m\033[30m" + "3.HEADER-Jogos模塊" + "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Jogos")]'))
            ).click()
            sleep(0.5)
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//button[contains(text(), "Telegrama")]'))
            ).click()
            #-------------------------3.1Telegram 
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Canal De")]'))
                )
                print("3.1 Telegram\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"3.1 跳轉Telegram失敗"+ "\033[0m")
            # 记录初始窗口句柄
            initial_window_handle = driver.current_window_handle
            elements = driver.find_elements(By.XPATH, "//*[contains(@class,'TelegramPage')]")
            if elements:
                elements[0].click()
            # 等待新窗口打开
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
            # 获取所有窗口句柄
            all_window_handles = driver.window_handles
            # 找到新窗口句柄
            new_window_handle = [handle for handle in all_window_handles if handle != initial_window_handle][0]
            # 切换到新窗口
            driver.switch_to.window(new_window_handle)
            # 这里可以进行新窗口中的操作
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.tgme_logo'))
                )
                print("3.1.2 Junte-se按鈕\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"3.1.2 Junte-se按鈕失效"+ "\033[0m")
            # 关闭新窗口
            driver.close()
            driver.switch_to.window(initial_window_handle)
            element=WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'[alt="Close Icon"]'))
            ).click()
            current_scroll_height = driver.execute_script("return window.pageYOffset;")
            # 使用 JavaScript 将页面滚动到顶部
            driver.execute_script("window.scrollTo(0, 0);")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//*[@data-icon= "left"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Todos')]"))
                )
                print("3.1.3 Telegram返回鍵\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"3.1.3 Telegram返回鍵失效"+ "\033[0m")

            #-------------------------3.2 Sobre Nós
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Jogos")]'))
            ).click()
            sleep(0.5)
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//button[contains(text(), "Sobre nós")]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Sobre Nós")]'))
                )
                print("3.2.1 Sobre Nós\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"3.2.1 跳轉Sobre Nós失敗"+ "\033[0m")
            # 找到目标元素
            target_element = driver.find_element(By.XPATH, '//div[contains(text(), "2015 Destino em Singapura")]')

            # 使用 ActionChains 模拟鼠标点击
            action = ActionChains(driver)
            action.click(target_element).perform()
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//*[@data-icon= "left"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Todos')]"))
                )
                print("3.2.2 Sobre Nós返回鍵\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"3.2.2 Sobre Nós返回鍵失效"+ "\033[0m")
            #-------------------------3.3 Gaming Curaçao
            '''
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Jogos")]'))
            ).click()
            sleep(0.5)
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//button[contains(text(), "Gaming Curaçao")]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Licença De Curaçao")]'))
                )
                print("3.3.1 Gaming Curaçao\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"3.3.1 跳轉Gaming Curaçao失敗"+ "\033[0m")
            # 找到目标元素
            target_element = driver.find_element(By.XPATH, '//img[@alt= "imageWithWaterMark"]')

            # 使用 ActionChains 模拟鼠标点击
            action = ActionChains(driver)
            action.click(target_element).perform()
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//*[@data-icon= "left"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Todos')]"))
                )
                print("3.3.2 Gaming Curaçao返回鍵\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"3.3.2 Gaming Curaçao返回鍵失效"+ "\033[0m")
            '''
            #-------------------------3.4 Jogos
            driver.back()
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Jogos")]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Slots")]'))
                )
                print("3.4 Jogos\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"3.4 跳轉Jogos失敗"+ "\033[0m")
            #-------------------------4.Atividade模塊
            print("\033[107m\033[30m" + "4.Atividade模塊" + "\033[0m")
            #-------------------------4.1 Check-in
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//button[contains(text(), "Check-in")]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Colete cupons")]'))
                )
                print("4.1 Check-in\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"4.1 跳轉Check-in失敗"+ "\033[0m")
            #-------------------------4.2 Primeiro depósito 20%
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Atividade")]'))
            ).click()
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Primeiro depósito")]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Primeira recarga")]'))
                )
                print("4.2.1 Primeiro depósito 20%\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"4.2.1 跳轉Primeiro depósito 20%失敗"+ "\033[0m")
            # 找到目标元素
            driver.refresh()
            sleep(0.5)
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//*[@data-icon= "left"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Todos')]"))
                )
                print("4.2.2 Primeiro depósito 20%返回鍵\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"4.2.2 Primeiro depósito 20%返回鍵失效"+ "\033[0m")
            driver.back()
            sleep(5)
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'ChargeButton')]"))
            ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"Balanço Total")]'))
                )
                print("4.2.3引導至儲值頁\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"4.2.3 引導至儲值頁失敗"+ "\033[0m")
            #-------------------------4.3 Recarregar Cashback 10%
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Atividade")]'))
            ).click()
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Recarregar Cashback")]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Recarga benefícios")]'))
                )
                print("4.3.1 Recarregar Cashback 10%\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"4.3.1 跳轉Recarregar Cashback 10%失敗"+ "\033[0m")
            # 找到目标元素
            driver.refresh()
            sleep(0.5)
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//*[@data-icon= "left"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Todos')]"))
                )
                print("4.3.2 Recarregar Cashback 10%返回鍵\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"4.3.2 Recarregar Cashback 10%返回鍵失效"+ "\033[0m")
            driver.back()
            sleep(1)
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'ChargeButton')]"))
            ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"Balanço Total")]'))
                )
                print("4.3.3引導至儲值頁\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"4.3.3 引導至儲值頁失敗"+ "\033[0m")
            #-------------------------5.Convidar模塊
            print("\033[107m\033[30m" + "5.Convidar模塊" + "\033[0m")
            element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Convidar")]'))
                    ).click()

            try:
            # 检查第一个元素是否存在
                div_element_invite = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Como convidar usuários?")]'))
            )
                print("5.Convidar模塊\033[32mOK\033[0m")
                    
            except TimeoutException:
                try:
                # 检查第二个元素是否存在
                    div_element_link = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Link exclusivo")]'))
                )
                    print("5.Convidar模塊\033[32mOK\033[0m")
                    print("\033[44m\033[97m" + "5.無接上邀請" + "\033[0m")
                except TimeoutException:
                # 两个元素都不存在的情况
                    print("\033[91m" +"5. 跳轉Convidar模塊失敗"+ "\033[0m")
            #-------------------------6.VIP模塊
            print("\033[107m\033[30m" + "6.VIP模塊" + "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "VIP")]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Meu progresso VIP")]'))
                )
                print("6.1 VIP模塊\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"6.1 跳轉VIP模塊失敗"+ "\033[0m")
            # 找到目标元素
            target_element = driver.find_element(By.XPATH,'//*[contains(text(), "Descrição do nível VIP")]')

            # 使用 ActionChains 模拟鼠标点击
            action = ActionChains(driver)
            action.click(target_element).perform()
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//*[@data-icon= "left"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Todos')]"))
                )
                print("6.2 VIP模塊返回鍵\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"6.2 VIP模塊返回鍵失效"+ "\033[0m")
            #-------------------------7.Download
            print("\033[107m\033[30m" + "7.Download" + "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Download")]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Baixar Android")]'))
                )
                print("7.Download\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"7.跳轉Download失敗"+ "\033[0m")
            driver.find_element(By.CSS_SELECTOR,'[alt="Close Icon"]').click()
            #-------------------------8.餘額欄位
            print("\033[107m\033[30m" + "8.餘額欄位" + "\033[0m")

            element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'img[alt="refresh"]'))
                    ).click()

            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "icon-loading")]'))
                )
                print("8.1重刷按鈕\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"8.1 重刷按鈕失效"+ "\033[0m")

            element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'img[alt="add"]'))
                    ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"Balanço Total")]'))
                )
                print("8.2引導至儲值頁\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"8.2 引導至儲值頁失敗"+ "\033[0m")
            #-------------------------9.個人資訊頁
            print("\033[107m\033[30m" + "9.個人資訊頁" + "\033[0m")
            element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//img[contains(@class,"Header__DirectionIcon")]'))
                    )
            action = ActionChains(driver)
            action.click(element).click(element).perform()
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"Registro Do Jogo")]'))
                )
                print("9.個人資訊頁\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"9. 跳轉個人資訊頁失敗"+ "\033[0m")
            #-------------------------10.通知中心
            print("\033[107m\033[30m" + "10.通知中心" + "\033[0m")
            element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt='notification']"))
                    ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"Centro de Notificação")]'))
                )
                print("10.通知中心\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"10. 跳轉通知中心失敗"+ "\033[0m")

            driver.refresh()
            sleep(1)
            #-------------------------11.遊戲logo
            print("\033[107m\033[30m" + "11.遊戲logo" + "\033[0m")
            element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt='logo-menu']"))
                    ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Slots')]"))
                )
                print("11.點擊遊戲logo跳轉首頁\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"11.點擊遊戲logo 失效"+ "\033[0m")
            print("\033[48;5;22m\033[97m" + "HEADER模塊OK" + "\033[0m")
            print("\033[43m\033[30m" + "廣告banner模塊" + "\033[0m")
            #-------------------------1.首充20%banner
            element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Go to slide 1']"))
                    ).click()
            sleep(0.5)
            element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt='banner_2']"))
                    )
            actions = ActionChains(driver)
            actions.click(element).perform() 
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Primeira recarga")]'))
                )
                print("1.首充20%banner\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.點擊首充20%banner 失效"+ "\033[0m")
            driver.back()
            #-------------------------2.充值10%banner
            element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Go to slide 2']"))
                    ).click()
            sleep(0.5)
            element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt='banner_2']"))
                    )
            actions = ActionChains(driver)
            actions.click(element).perform() 
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Recarga benefícios")]'))
                )
                print("2.充值10%banner\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"2.點擊充值10%banner 失效"+ "\033[0m")
            driver.back()
        #-------------------------3.邀請banner
            element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Go to slide 3']"))
                    ).click()
            sleep(0.5)
            element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt='banner_3']"))
                    )
            actions = ActionChains(driver)
            actions.click(element).perform() 
            try:
            # 检查第一个元素是否存在
                div_element_invite = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Como convidar usuários?")]'))
            )
                print("3.邀請banner模塊\033[32mOK\033[0m")
                print("\033[44m\033[97m" + "3.無接上寶箱" + "\033[0m")
            except TimeoutException:
                try:
                # 检查第二个元素是否存在
                    div_element_link = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Link exclusivo")]'))
                )
                    print("3.邀請banner模塊\033[32mOK\033[0m")
                    print("\033[44m\033[97m" + "3.無接上邀請" + "\033[0m")
                except TimeoutException:
                # 两个元素都不存在的情况
                    print("\033[91m" +"3.邀請banner模塊失敗"+ "\033[0m")
            driver.back()
            #-------------------------4.VIP banner
            '''
            element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Go to slide 4']"))
                    ).click()
            sleep(0.5)
            element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt='banner_4']"))
                    )
            actions = ActionChains(driver)
            actions.click(element).perform() 
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Meu progresso VIP")]'))
                )
                print("4.VIP banner\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"4. 點擊VIP banner失敗"+ "\033[0m")
            driver.back()
            '''
            #-------------------------5.報到banner
            '''
            element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Go to slide 5']"))
                    ).click()
            sleep(0.5)
            element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt='banner_5']"))
                    )
            actions = ActionChains(driver)
            actions.click(element).perform() 
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Como convidar usuários?")]'))
                )
                print("5.報到banner\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"5. 點擊報到banner失敗"+ "\033[0m")
            driver.back()
            print("\033[48;5;22m\033[97m" + "Banner模塊OK" + "\033[0m")
            '''
            print("\033[43m\033[30m" + "遊戲filter模塊" + "\033[0m")
            #-------------------------1.Filter_slot
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "ImageTab")]//span[contains(text(), "Slots")]'))
                )
                element.click()

                # 在点击后，尝试查找下一个元素，找到则执行相应的操作
                try:
                    div_element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "PG-Slots")]'))
                    )
                    print("1.Filter_slot\033[32mOK\033[0m")
                except TimeoutException:
                    print("\033[91m" +"1. 點擊Filter_slot失敗"+ "\033[0m")

            except TimeoutException:
                # 找不到第一个元素的处理
                print("\033[44m\033[97m" + "1.無接上slot" + "\033[0m")
            #-------------------------2.Filter_Fishing
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "ImageTab")]//span[contains(text(), "Fishing")]'))
                )
                element.click()

                # 在点击后，尝试查找下一个元素，找到则执行相应的操作
                try:
                    div_element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "JILI-Fishing")]'))
                    )
                    print("2.Filter_Fishing\033[32mOK\033[0m")
                except TimeoutException:
                    print("\033[91m" +"2. 點擊Filter_Fishing失敗"+ "\033[0m")

            except TimeoutException:
                # 找不到第一个元素的处理
                print("\033[44m\033[97m" + "2.無接上Fishing" + "\033[0m")
            #-------------------------3.Filter_Viver
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "ImageTab")]//span[contains(text(), "Viver")]'))
                )
                element.click()

                # 在点击后，尝试查找下一个元素，找到则执行相应的操作
                try:
                    div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "PP-Viver")]'))
                )
                    print("3.Filter_Viver\033[32mOK\033[0m")
                except TimeoutException:
                    print("\033[91m" +"3. 點擊Filter_Viver失敗"+ "\033[0m")

            except TimeoutException:
                # 找不到第一个元素的处理
                print("\033[44m\033[97m" + "3.無接上Viver" + "\033[0m")
            #-------------------------4.Filter_Favoritos
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "ImageTab")]//span[contains(text(), "Favoritos")]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Favoritos")]'))
                )
                print("4.Filter_Favoritos\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"4. 點擊Filter_Favoritos失敗"+ "\033[0m")
            #-------------------------5.Filter_Todos
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "ImageTab")]//span[text()= "Todos"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Slots")]'))
                )
                print("5.Filter_Todos\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"5. 點擊Filter_Todos失敗"+ "\033[0m")
            #-------------------------6.搜尋欄位
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[contains(@class, "InputSection")]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[text()= "Procurar"]'))
                )
                print("6.搜尋欄位\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"6. 點擊搜尋欄位失敗"+ "\033[0m")
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt='Close Icon']"))
            ).click()
            #-------------------------7.Filter_Arcades
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "ImageTab")]//span[text()= "Arcades"]'))
                )
                element.click()

                # 在点击后，尝试查找下一个元素，找到则执行相应的操作
                try:
                    div_element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "FC-Arcade")]'))
                    )
                    print("7.Filter_Arcades \033[32mOK\033[0m")
                except TimeoutException:
                    print("\033[91m7.Filter_Arcades失敗\033[0m")

            except TimeoutException:
                # 找不到第一个元素的处理
                print("\033[44m\033[97m" + "7.無接上Arcades" + "\033[0m")
            #-------------------------8.Filter_Tables
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "ImageTab")]//span[text()= "Tables"]'))
                )
                element.click()

                # 在点击后，尝试查找下一个元素，找到则执行相应的操作
                try:
                    div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "FC-Table")]'))
                )
                    print("8.Filter_Tables\033[32mOK\033[0m")
                except TimeoutException:
                    print("\033[91m" +"8.Filter_Tables失敗"+ "\033[0m")

            except TimeoutException:
                # 找不到第一个元素的处理
                print("\033[44m\033[97m" + "8.無接上Tables" + "\033[0m")
            #-------------------------9.Filter_Cards
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "ImageTab")]//span[text()= "Cards"]'))
                )
                element.click()

                # 在点击后，尝试查找下一个元素，找到则执行相应的操作
                try:
                    div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "-Cards")]'))
                )
                    print("9.Filter_Cards\033[32mOK\033[0m")
                except TimeoutException:
                    print("\033[91m" +"9.Filter_Cards失敗"+ "\033[0m")

            except TimeoutException:
                # 找不到第一个元素的处理
                print("\033[44m\033[97m" + "9.無接上Cards" + "\033[0m")

            print("\033[48;5;22m\033[97m" + "遊戲filter模塊OK" + "\033[0m")

            print("\033[43m\033[30m" + "Footer模塊" + "\033[0m")
            #-------------------------10.Filter_Bingo
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "ImageTab")]//span[text()= "Bingo"]'))
                )
                element.click()

                # 在点击后，尝试查找下一个元素，找到则执行相应的操作
                try:
                    div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "-Bingo")]'))
                )
                    print("10.Filter_Bingo\033[32mOK\033[0m")
                except TimeoutException:
                    print("\033[91m" +"10.Filter_Bingo失敗"+ "\033[0m")

            except TimeoutException:
                # 找不到第一个元素的处理
                print("\033[44m\033[97m" + "10.無接上Bingo" + "\033[0m")

            print("\033[48;5;22m\033[97m" + "遊戲filter模塊OK" + "\033[0m")

            print("\033[43m\033[30m" + "Footer模塊" + "\033[0m")
            #-------------------------1.Jogo_Slots
            #先判斷Header位置
            target_element = driver.find_element(By.XPATH,'//div[contains(text(), "Download")]')  

            element_location = target_element.location

            script = """
            return {
                width: window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth,
                height: window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight
            };
            """
            result = driver.execute_script(script)
            page_width = result['width']
            page_height = result['height']

            element_x_in_full_screen = element_location['x']
            element_y_in_full_screen = element_location['y']
            #-------------------------1.Jogo_Slots
            try:
                element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Slots")]'))
            ).click()
                sleep(1)
            
                # 等待元素出现
                try:
                    div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Go to slide 1']"))
                ).click()
                    print("\033[91m" +"1.1 Jogo_Slots置頂失效"+ "\033[0m")
                except Exception as e:
                    # 点击失败则表示元素可见但不可点击
                    print("1.1 Jogo_Slots置頂\033[32mOK\033[0m")
                try:
                        div_element = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "-Slots")]'))
                        )
                        print("1.2 Jogo_Slots_filter \033[32mOK\033[0m")
                except TimeoutException:
                        print("\033[91m" +"1.2. Jogo_Slots_filter失效"+ "\033[0m")
            except TimeoutException:
                # 元素未出现
                print("\033[91m" +"1.無接上slot"+ "\033[0m")
            #-------------------------2.Jogo_Salão
            #點footer按鈕
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Salão")]'))
            ).click()
            sleep(1)
            # 等待元素出现
            div_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Go to slide 1']"))
            )

            try:
                # 尝试点击元素
                div_element.click()
                print("\033[91m" +"2.1 Jogo_Salão置頂失效"+ "\033[0m")
            except Exception as e:
                # 点击失败则表示元素可见但不可点击
                print("2.1 Jogo_Salão置頂\033[32mOK\033[0m")
            try:
                    div_element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//span[@class="flex flex-row items-center" and .="Slots"]'))
                    )
                    print("2.2 Jogo_Salão_filter \033[32mOK\033[0m")
            except TimeoutException:
                    print("\033[91m" +"2.2. Jogo_Salão_filter失效"+ "\033[0m")
            #-------------------------3.Jogo_Fishing
            try:
                element = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Fishing")]'))
                        ).click()
                sleep(1)
            
                # 等待元素出现
                try:
                    div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Go to slide 1']"))
                ).click()
                    print("\033[91m" +"3.1 Jogo_Fishing置頂失效"+ "\033[0m")
                except Exception as e:
                    # 点击失败则表示元素可见但不可点击
                    print("3.1 Jogo_Fishing置頂\033[32mOK\033[0m")
                try:
                        div_element = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "-Fishing")]'))
                        )
                        print("3.2 Jogo_Fishing_filter \033[32mOK\033[0m")
                except TimeoutException:
                        print("\033[91m" +"3.2. Jogo_Fishing_filter失效"+ "\033[0m")
            except TimeoutException:
                # 元素未出现
                print("\033[44m\033[97m" + "3.無接上Fishing" + "\033[0m")
            #-------------------------4.Jogo_Viver
            try:
                element = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Viver")]'))
                        ).click()
                sleep(1)
            
                # 等待元素出现
                try:
                    div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Go to slide 1']"))
                ).click()
                    print("\033[91m" +"4.1 Jogo_Viver置頂失效"+ "\033[0m")
                except Exception as e:
                    # 点击失败则表示元素可见但不可点击
                    print("4.1 Jogo_Viver置頂\033[32mOK\033[0m")
                try:
                        div_element = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "-Viver")]'))
                        )
                        print("4.2 Jogo_Viver_filter \033[32mOK\033[0m")
                except TimeoutException:
                        print("\033[91m" +"4.2. Jogo_Viver_filter失效"+ "\033[0m")
            except TimeoutException:
                # 元素未出现
                print("\033[44m\033[97m" + "4.無接上Viver" + "\033[0m")
            #-------------------------5.Jogo_Arcades
            try:
                element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Arcades")]'))
                    ).click()
                sleep(1)
            
                # 等待元素出现
                try:
                    div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Go to slide 1']"))
                ).click()
                    print("\033[91m" +"5.1 Jogo_Arcades置頂失效"+ "\033[0m")
                except Exception as e:
                    # 点击失败则表示元素可见但不可点击
                    print("5.1 Jogo_Arcades置頂\033[32mOK\033[0m")
                try:
                        div_element = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "-Arcade")]'))
                        )
                        print("5.2 Jogo_Arcades \033[32mOK\033[0m")
                except TimeoutException:
                        print("\033[91m" +"5.2 Jogo_Arcades失效"+ "\033[0m")

            except TimeoutException:
                    # 找不到第一个元素的处理
                    print("\033[44m\033[97m" + "5. 無接上Arcades" + "\033[0m")
            #-------------------------6.Jogo_Tables
            try:
                element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Tables")]'))
                    ).click()
                sleep(1)
            
                # 等待元素出现
                try:
                    div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Go to slide 1']"))
                ).click()
                    print("\033[91m" +"6.1 Jogo_Tables置頂失效"+ "\033[0m")
                except Exception as e:
                    # 点击失败则表示元素可见但不可点击
                    print("6.1 Jogo_Tables置頂\033[32mOK\033[0m")
                try:
                        div_element = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "-Table")]'))
                        )
                        print("6.2 Jogo_Tables \033[32mOK\033[0m")
                except TimeoutException:
                        print("\033[91m" +"6.2 Jogo_Tables失效"+ "\033[0m")
                    
            except TimeoutException:
                    # 找不到第一个元素的处理
                    print("\033[44m\033[97m" + "6.無接上Tables" + "\033[0m")
            #-------------------------7.Jogo_Cards
            try:
                element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Cards")]'))
                    ).click()
                sleep(1)
            
                # 等待元素出现
                try:
                    div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Go to slide 1']"))
                ).click()
                    print("\033[91m" +"7.1 Jogo_Cards置頂失效"+ "\033[0m")
                except Exception as e:
                    # 点击失败则表示元素可见但不可点击
                    print("7.1 Jogo_Cards置頂\033[32mOK\033[0m")
                try:
                        div_element = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "-Cards")]'))
                        )
                        print("7.2 Jogo_Cards \033[32mOK\033[0m")
                except TimeoutException:
                        print("\033[91m" +"7.2 Jogo_Cards失效"+ "\033[0m")
                    
            except TimeoutException:
                    # 找不到第一个元素的处理
                    print("\033[44m\033[97m" + "7.無接上Jogo_Cards" + "\033[0m")

            #-------------------------8.Ajuda_Politica
            #點footer按鈕
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Politica de Privacidade")]'))
            ).click()
            sleep(1)
            # 判斷是否置頂
            target_x = element_x_in_full_screen
            target_y = element_y_in_full_screen
            target_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Download")]'))
                )

            element_location = target_element.location

            if target_x <= element_location['x'] <= target_x + target_element.size['width'] and \
                        target_y <= element_location['y'] <= target_y + target_element.size['height']:

                    print("8.1 Ajuda_Politica置頂\033[32mOK\033[0m")
            else:
                    print("\033[91m" +"8.1 Ajuda_Politica置頂失效"+ "\033[0m")
            #判斷filter功能
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Privacy Policy and Personal Data Protection")]'))
                )
                print("8.2 Politica 頁面 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"8.2 跳轉Politica失效"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//*[@data-icon= "left"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Todos')]"))
                )
                print("8.3 Politica返回鍵\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"8.3 Politica返回鍵返回鍵失效"+ "\033[0m")
            #-------------------------9.Ajuda_Termos
            #點footer按鈕
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Termos de Servico")]'))
            ).click()
            sleep(1)
            # 判斷是否置頂
            target_x = element_x_in_full_screen
            target_y = element_y_in_full_screen
            target_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Download")]'))
                )

            element_location = target_element.location

            if target_x <= element_location['x'] <= target_x + target_element.size['width'] and \
                        target_y <= element_location['y'] <= target_y + target_element.size['height']:

                    print("9.1 Ajuda_Termos置頂\033[32mOK\033[0m")
            else:
                    print("\033[91m" +"9.1 Ajuda_Termos置頂失效"+ "\033[0m")
            #判斷filter功能
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Termos de Serviço")]'))
                )
                print("9.2 Termos 頁面 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"9.2 跳轉Termos失效"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//*[@data-icon= "left"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Todos')]"))
                )
                print("9.3 Termos返回鍵\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"9.3 Termos返回鍵返回鍵失效"+ "\033[0m")
            #-------------------------10.Ajuda_Descrico
            #點footer按鈕
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Descrico do nivel VIP")]'))
            ).click()
            sleep(1)
            # 判斷是否置頂
            target_x = element_x_in_full_screen
            target_y = element_y_in_full_screen
            target_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Download")]'))
                )

            element_location = target_element.location

            if target_x <= element_location['x'] <= target_x + target_element.size['width'] and \
                        target_y <= element_location['y'] <= target_y + target_element.size['height']:

                    print("10.1 Ajuda_Descrico置頂\033[32mOK\033[0m")
            else:
                    print("\033[91m" +"10.1 Ajuda_Descrico置頂失效"+ "\033[0m")
            #判斷filter功能
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Meu progresso VIP")]'))
                )
                print("10.2 Descrico 頁面 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"10.2 跳轉Descrico失效"+ "\033[0m")
            #-------------------------11.外網連結_Skrill
            # 记录初始窗口句柄
            initial_window_handle = driver.current_window_handle

            element=WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.XPATH, "//img[contains(@src,'footer3')]"))
                ).click()

            # 等待新窗口打开
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
            # 获取所有窗口句柄
            all_window_handles = driver.window_handles
            # 找到新窗口句柄
            new_window_handle = [handle for handle in all_window_handles if handle != initial_window_handle][0]
            # 切换到新窗口
            driver.switch_to.window(new_window_handle)
            # 这里可以进行新窗口中的操作
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//img[@alt= "Skrill Logo"]'))
                )
                print("11.外網連結_Skrill 頁面 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"11. 跳轉外網連結_Skrill失效"+ "\033[0m")
                # 打印错误消息后，继续执行，直接跳过
            pass
            # 关闭新窗口
            driver.close()
            # 切换回原始窗口
            driver.switch_to.window(initial_window_handle)
            #-------------------------12.外網連結_BeGambleAware
            element=WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.XPATH, "//img[contains(@src,'footer5')]"))
                ).click()

            # 等待新窗口打开
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
            # 获取所有窗口句柄
            all_window_handles = driver.window_handles
            # 找到新窗口句柄
            new_window_handle = [handle for handle in all_window_handles if handle != initial_window_handle][0]
            # 切换到新窗口
            driver.switch_to.window(new_window_handle)
            # 这里可以进行新窗口中的操作
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//img[@alt= "Logo for \'BeGambleAware\'"]'))
                )
                print("12.外網連結_BeGambleAware 頁面 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"12. 跳轉外網連結_BeGambleAware失效"+ "\033[0m")
            # 关闭新窗口
            driver.close()
            # 切换回原始窗口
            driver.switch_to.window(initial_window_handle)
            #-------------------------13.外網連結_Interac
            element=WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.XPATH, "//img[contains(@src,'footer6')]"))
                ).click()

            # 等待新窗口打开
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
            # 获取所有窗口句柄
            all_window_handles = driver.window_handles
            # 找到新窗口句柄
            new_window_handle = [handle for handle in all_window_handles if handle != initial_window_handle][0]
            # 切换到新窗口
            driver.switch_to.window(new_window_handle)
            # 这里可以进行新窗口中的操作
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//a[@title= "Interac"]'))
                )
                print("13.外網連結_Interac 頁面 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"13. 跳轉外網連結_Interac失效"+ "\033[0m")
            # 关闭新窗口
            driver.close()
            # 切换回原始窗口
            driver.switch_to.window(initial_window_handle)    
            #-------------------------14.外網連結_GamCare
            element=WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.XPATH, "//img[contains(@src,'footer4')]"))
                ).click()

            # 等待新窗口打开
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
            # 获取所有窗口句柄
            all_window_handles = driver.window_handles
            # 找到新窗口句柄
            new_window_handle = [handle for handle in all_window_handles if handle != initial_window_handle][0]
            # 切换到新窗口
            driver.switch_to.window(new_window_handle)
            # 这里可以进行新窗口中的操作
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//img[@alt= "GamCare logo"]'))
                )
                print("14.外網連結_GamCare 頁面 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"14. 跳轉外網連結_GamCare 頁面失效"+ "\033[0m")
            # 关闭新窗口
            driver.close()
            # 切换回原始窗口
            driver.switch_to.window(initial_window_handle) 
            #-------------------------15.Footer_icon_Gaming Curaçao
            element=WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "img[src='/license.06fdfd1ababef6ef.png']"))
                ).click()  
            sleep(1)
            # 判斷是否置頂
            target_x = element_x_in_full_screen
            target_y = element_y_in_full_screen
            target_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Download")]'))
                )

            element_location = target_element.location

            if target_x <= element_location['x'] <= target_x + target_element.size['width'] and \
                        target_y <= element_location['y'] <= target_y + target_element.size['height']:

                    print("15.1 Footer_icon_Gaming Curaçao置頂\033[32mOK\033[0m")
            else:
                    print("\033[91m" +"15.1 Footer_icon_Gaming Curaçao置頂失效"+ "\033[0m")
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Licença De Curaçao")]'))
                )
                print("15.2 Footer_icon_Gaming Curaçao\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"15.2 Footer_icon_Gaming Curaçao失效"+ "\033[0m") 
            #-------------------------16.Footer文案收合
            element=WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.XPATH, "//button[text()='Mostrar']"))
                ).click()  
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Colocar fora")]'))
                )
                print("16.Footer文案收合\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"16. Footer文案收合失效"+ "\033[0m")
            print("\033[48;5;22m\033[97m" + "Footer模塊OK" + "\033[0m")

            print("\033[43m\033[30m" + "浮動按鈕模塊" + "\033[0m")
            #-------------------------1.Download按鈕
            element=WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.XPATH, "//img[@alt='download']"))
                ).click()  
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Baixar Android")]'))
                )
                print("1.Download按鈕\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.Download按鈕失效"+ "\033[0m")
            element=WebDriverWait(driver,5).until(
                EC.presence_of_element_located((By.XPATH, "//img[@alt='Close Icon']"))
                ).click()  
            #-------------------------2.Telegram按鈕
            # 记录初始窗口句柄
            initial_window_handle = driver.current_window_handle
            elements = driver.find_elements(By.XPATH, "//img[@alt='telegram']")
            if elements:
                elements[0].click()
            # 等待新窗口打开
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
            # 获取所有窗口句柄
            all_window_handles = driver.window_handles
            # 找到新窗口句柄
            new_window_handle = [handle for handle in all_window_handles if handle != initial_window_handle][0]
            # 切换到新窗口
            driver.switch_to.window(new_window_handle)
            # 这里可以进行新窗口中的操作
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.tgme_logo'))
                )
                print("2.1Telegram_Serviço按鈕\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"2.1Telegram_Serviço按鈕失效"+ "\033[0m")
            # 关闭新窗口
            driver.close()
            # 切换回原始窗口
            driver.switch_to.window(initial_window_handle)
            # 记录初始窗口句柄
            initial_window_handle = driver.current_window_handle
            elements = driver.find_elements(By.XPATH, "//img[@alt='telegram']")
            if elements:
                elements[1].click()
            # 等待新窗口打开
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
            # 获取所有窗口句柄
            all_window_handles = driver.window_handles
            # 找到新窗口句柄
            new_window_handle = [handle for handle in all_window_handles if handle != initial_window_handle][0]
            # 切换到新窗口
            driver.switch_to.window(new_window_handle)
            # 这里可以进行新窗口中的操作
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.tgme_logo'))
                )
                print("2.2Telegram_Gerente按鈕\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"2.2Telegram_Gerente按鈕失效"+ "\033[0m")
            # 关闭新窗口
            driver.close()
            # 切换回原始窗口
            driver.switch_to.window(initial_window_handle)

            print("\033[48;5;22m\033[97m" + "浮動按鈕模塊OK" + "\033[0m")
            # 打印统计结果和带颜色的百分比
            total_percentage = sys.stdout.total_count / sys.stdout.total_count * 100
            green_percentage = sys.stdout.green_count / sys.stdout.total_count * 100
            red_percentage = sys.stdout.red_count / sys.stdout.total_count * 100
            print("測試項目"+ "\033[93m"f"{ui_version}{product}"+"\033[0m")
            print(f"總測試筆數: {sys.stdout.total_count} ({total_percentage:.2f}%)")
            print(f"\033[32m測試成功筆數: {sys.stdout.green_count} ({green_percentage:.2f}%)\033[0m")
            print(f"\033[91m測試失敗筆數: {sys.stdout.red_count} ({red_percentage:.2f}%)\033[0m")
    #<<<<<<<<<<<<<<<<<<<<<背景偵測popup，結束>>>>>>>>>>>>>>>>>>>>>>
        except TimeoutException:
                pass
        finally:
                exit_event.set()
                popup_thread.join() 
#<<<<<<<<<<<<<<<<<<<<<背景偵測popup，結束>>>>>>>>>>>>>>>>>>>>>>
if __name__ == "__main__":
    main()