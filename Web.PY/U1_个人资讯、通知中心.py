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
import time
import sys
import threading
import pyperclip
import re
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
product_numbers = ['VV']

def main():
    # 初始化Chrome浏览器
    driver = webdriver.Chrome()

    for product in product_numbers:
        url = config.get(ui_version, product)
        sys.stdout.reset_counts()

        # 打开网页
        driver.get(url)
        WebDriverWait(driver, 10)
        driver.maximize_window()
#<<<<<<<<<<<<<<<<<<<<<背景偵測popup，開始>>>>>>>>>>>>>>>>>>>>>>
        popup_thread = threading.Thread(target=handle_popups, args=(driver,))
        popup_thread.start()
#<<<<<<<<<<<<<<<<<<<<<背景偵測popup，開始>>>>>>>>>>>>>>>>>>>>>>
#1. 个人资讯页---------------------------------------------------------
        try:
            print("\033[43m\033[30m" + "1. 个人资讯页" + "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[type="number"]'))
            ).send_keys('99999990000')
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[type="password"]'))
            ).send_keys('1111')
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "ConfirmButton")]'))
            ).click()
            sleep(8)
            element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//section[contains(@class,"flex gap-2 items-center")]'))
                )
            ActionChains(driver).double_click(element).perform() 
#1.1 複製ID按鈕---------------------------------------------------------
            print("\033[107m\033[30m" + "1.1 複製ID按鈕" + "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//span[@aria-label= "copy"]'))
                        ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="Copiado!"]')))
                print("1.1.1 複製ID按鈕 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.1.1 複製ID按鈕失效"+ "\033[0m")
            try:
                clipboard_content = pyperclip.paste()
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//div[@class="flex gap-2 text-lg items-center"]'))
                        )
                element_text = element.text
                number = re.search(r'\d+', element_text).group()
                if clipboard_content == number:
                    print("1.1.2 複製功能 \033[32mOK\033[0m")
                else:
                    print("\033[91m" +"1.1.2 複製功能失效"+ "\033[0m")
            except TimeoutException:
                print("未找到複製內容\033[0m")
#1.2 登出功能---------------------------------------------------------
            print("\033[107m\033[30m" + "1.2 登出功能" + "\033[0m")
            element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//img[@src="assets/u1/ic_sign_out.png"]'))
                ).click()
            element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Cancelar")]'))
            ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//section[contains(@class,"flex gap-2 items-center")]')))
                print("1.2.1 登出取消 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.2.1 登出取消失效"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//section[contains(@class,"flex gap-2 items-center")]'))
                )
            ActionChains(driver).double_click(element).perform() 
            element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//img[@src="assets/u1/ic_sign_out.png"]'))
                ).click()
            element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Confirme")]'))
            ).click()
            try:
                EC.presence_of_element_locatedelement = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//span[contains(text(), "Entrar")]')))
  
                print("1.2.2 登出確認 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.2.2 登出確認失效"+ "\033[0m")
#1.3 VIP、充值提現頁、邀請功能---------------------------------------------------------
            print("\033[107m\033[30m" + "1.3 VIP、充值提現頁、邀請功能" + "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[type="number"]'))
            ).send_keys('99999990000')
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[type="password"]'))
            ).send_keys('1111')
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "ConfirmButton")]'))
            ).click()
            sleep(2)
            element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//section[contains(@class,"flex gap-2 items-center")]'))
                )
            ActionChains(driver).double_click(element).perform() 
            elements = driver.find_elements(By.XPATH, '//span[@class= "anticon anticon-right"]')
            if elements:
                elements[0].click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[text()="Meu progresso VIP"]')))
                print("1.3.1 VIP頁引導 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.3.1 VIP頁引導失效"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//section[contains(@class,"flex gap-2 items-center")]'))
                )
            ActionChains(driver).double_click(element).perform() 
            elements = driver.find_elements(By.XPATH, '//span[@class= "anticon anticon-right"]')
            if elements:
                elements[1].click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[text()="Depositar conta"]')))
                print("1.3.2 充值提現頁引導 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.3.2 充值提現頁引導失效"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//section[contains(@class,"flex gap-2 items-center")]'))
                )
            ActionChains(driver).double_click(element).perform() 
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "button-withdraw")]'))
            ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//label[text()="Nome do titular da conta"]')))
                print("1.3.3 提現頁引導 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.3.3 提現頁引導失效"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//section[contains(@class,"flex gap-2 items-center")]'))
                )
            ActionChains(driver).double_click(element).perform() 
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "button-deposit")]'))
            ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"Prezado usuário")]')))
                print("1.3.4 充值頁引導 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.3.4 充值頁引導失效"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//section[contains(@class,"flex gap-2 items-center")]'))
                )
            ActionChains(driver).double_click(element).perform() 
            elements = driver.find_elements(By.XPATH, '//span[@class= "anticon anticon-right"]')
            if elements:
                elements[2].click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[text()="Como convidar usuários?"]')))
                print("1.3.5 邀請頁引導 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.3.5 邀請頁引導失效"+ "\033[0m")
#1.4 遊戲紀錄、更改個資頁---------------------------------------------------------
            print("\033[107m\033[30m" + "1.4 遊戲紀錄、更改個資頁" + "\033[0m")
            element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//section[contains(@class,"flex gap-2 items-center")]'))
                )
            ActionChains(driver).double_click(element).perform() 
            elements = driver.find_elements(By.XPATH, '//span[@class= "anticon anticon-right"]')
            if elements:
                elements[3].click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//th[text()="Nome do jogo"]')))
                print("1.4.1 遊戲紀錄頁引導 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.4.1 遊戲紀錄頁失效"+ "\033[0m")
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "ant-picker ant-picker-range")]'))
            ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "ant-picker-date-panel")]'))
            )
                print("1.4.2 遊戲紀錄月曆開啟 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.4.2 遊戲紀錄月曆開啟失效"+ "\033[0m")
            button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[text()= "Retornar"]'))
            )
            ActionChains(driver).double_click(button).perform()
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//span[@aria-label= "left"]'))
            ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//span[text()= "Slots"]'))
            )
                print("1.4.3 遊戲紀錄返回鍵 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.4.3 遊戲紀錄返回鍵失效"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//section[contains(@class,"flex gap-2 items-center")]'))
                )
            ActionChains(driver).double_click(element).perform() 
            elements = driver.find_elements(By.XPATH, '//span[@class= "anticon anticon-right"]')
            if elements:
                elements[4].click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="Número de telefone"]')))
                print("1.4.4 更改個資頁引導 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.4.4 更改個資頁失效"+ "\033[0m")
            
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(((By.XPATH, '//*[text()="Editar"]')))
            ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="Alterar apelido favrito"]')))
                print("1.4.5 更改ID彈窗 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.4.5 更改ID彈窗失效"+ "\033[0m")
            sleep(1)
            avatar_button = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//img[@alt="avatar11"]'))
                    )
            ActionChains(driver).click(avatar_button).perform()
            # 获取第一个头像的 src 属性值
            avatar_src = avatar_button.get_attribute("src")
            # 点击按钮
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="Cancelar"]')))
            ActionChains(driver).click(button).perform() 
            sleep(1)
            avatar_img = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//img[@alt="avatar"]'))) 
            # 获取第二个头像的 src 属性值
            avatar_src1 = avatar_img.get_attribute("src")
            # 比较两个头像的 src 属性值是否相等
            if avatar_src == avatar_src1:
                print("\033[91m" +"1.4.6 更換頭像送出取消失敗"+ "\033[0m")
            else:
                print("1.4.6 更換頭像送出取消成功 \033[32mOK\033[0m")
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(((By.XPATH, '//*[text()="Editar"]')))
            ).click()
            sleep(1)
            avatar_button = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//img[@alt="avatar9"]'))
                    )
            ActionChains(driver).click(avatar_button).perform()
            avatar_src = avatar_button.get_attribute("src")
            sleep(1)
            # 点击按钮
            button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[contains(@class,"EditUserInfoModal__ConfirmButton-pzt32c-1")]'))
            )
            ActionChains(driver).click(button).perform()
            # 等待第二个头像出现
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="Done"]')))
                print("1.4.7 更換頭像送出提示 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.4.7 更換頭像送出提示未顯示"+ "\033[0m")
            avatar_img = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//img[@alt="avatar"]'))) 
            # 获取第二个头像的 src 属性值
            avatar_src1 = avatar_img.get_attribute("src")
            # 比较两个头像的 src 属性值是否相等
            if avatar_src == avatar_src1:
                print("1.4.8 更換頭像送出成功1 \033[32mOK\033[0m")
            else:
                print("\033[91m" +"1.4.8 更換頭像送出1失敗"+ "\033[0m")
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(((By.XPATH, '//*[text()="Editar"]')))
            ).click()
            sleep(1)
            avatar_button = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//img[@alt="avatar12"]'))
                    )
            ActionChains(driver).click(avatar_button).perform()
            # 获取第一个头像的 src 属性值
            avatar_src = avatar_button.get_attribute("src")
            # 点击按钮
            button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[text()="Confirme" or text()="Cargando"]'))
            )
            ActionChains(driver).click(button).perform()
            sleep(1)
            avatar_img = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//img[@alt="avatar"]'))) 
            # 获取第二个头像的 src 属性值
            avatar_src1 = avatar_img.get_attribute("src")
            # 比较两个头像的 src 属性值是否相等
            if avatar_src == avatar_src1:
                print("1.4.9 更換頭像送出成功2 \033[32mOK\033[0m")
            else:
                print("\033[91m" +"1.4.9 更換頭像送出2失敗"+ "\033[0m")
            
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(((By.XPATH, '//*[text()="Editar"]')))
            ).click()
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(((By.XPATH, '//*[contains(@class,"input-placeholder-color")]')))
            )
            action_chains = ActionChains(driver)
            action_chains.click(button).send_keys(Keys.BACKSPACE * 4).perform()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="Insira um apelido"]')))
                print("1.4.10 ID更改欄位空白 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.4.10 ID更改欄位空白未顯示錯誤訊息"+ "\033[0m")
            button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(((By.XPATH, '//*[contains(@class,"input-placeholder-color")]')))
            ).send_keys("12345")
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="nome de usuário (6-16 letras e números)"]')))
                print("1.4.11 ID更改欄位5碼 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.4.11 ID更改欄位5碼未顯示錯誤訊息"+ "\033[0m")
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(((By.XPATH, '//*[contains(@class,"input-placeholder-color")]')))
            ).send_keys("678901234567")
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="nome de usuário (6-16 letras e números)"]')))
                print("1.4.12 ID更改欄位17碼 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.4.12 ID更改欄位17碼未顯示錯誤訊息"+ "\033[0m")
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(((By.XPATH, '//*[contains(@class,"input-placeholder-color")]')))
            )
            action_chains.click(button).send_keys(Keys.BACKSPACE * 1).perform()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="nome de usuário (6-16 letras e números)"]')))
                print("\033[91m" +"1.4.13 ID更改欄位16碼顯示錯誤訊息"+ "\033[0m")
            except TimeoutException:
                print("1.4.13 ID更改欄位16碼無錯誤訊息 \033[32mOK\033[0m")
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="Confirme"]'))
            ).click()
            # 等待第二个头像出现
            sleep(1)
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="Done"]')))
                print("1.4.14 更換ID送出提示 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.4.14 更換ID送出提示未顯示"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@class="text-lg text-white flex gap-2"]')))
            element1=element.text
            if element1 == "1234567890123456":
                print("1.4.15 更換ID成功 \033[32mOK\033[0m")
            else:    
                print("\033[91m" +"1.4.15 更換ID失敗"+ "\033[0m")
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(((By.XPATH, '//*[text()="Editar"]')))
            ).click()
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(((By.XPATH, '//img[@alt="Close Icon"]')))
            ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="Número de telefone"]')))
                print("1.4.16 X icon功能 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.4.16 X icon功能失效"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//span[@class= "anticon anticon-right"]'))
                ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="2. About this Policy"]')))
                print("1.4.17 隱私頁跳轉 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.4.17 隱私頁跳轉失效"+ "\033[0m")
            driver.back()
            button = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//span[@aria-label= "left"]'))
                    ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//span[text()="Slots"]')))
                print("1.4.18 更改個資頁返回鍵 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.4.18 更改個資頁返回鍵失效"+ "\033[0m")
#2. 通知---------------------------------------------------------
            print("\033[43m\033[30m" + "2. 通知" + "\033[0m")
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@alt= "notification"]'))
            ).click()
            elements = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@class,'NotificationItemRedDot')]"))
            )
            count = len(elements) 
            element1 = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(@class,"MessageCountBadge")]')))
            element2 = int(element1.text)    
            if element2 == count:
                print("2.1 通知未讀數量 \033[32mOK\033[0m")
            else:
                print("\033[91m" +"2.1 通知未讀數量錯誤"+ "\033[0m")
            elements = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@class,'NotificationItemRedDot')]"))
            )
            if elements:
                elements[1].click()
            elements = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@class,'NotificationItemExpandable')]"))
            )
            count1 = len(elements)
            elements = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@class,'NotificationItemRedDot')]"))
            )
            if elements:
                elements[0].click()
            elements = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@class,'NotificationItemExpandable')]"))
            )
            count2 = len(elements)        
            if count2 == count1 == 1:
                print("2.2 一次開啟一封通知 \033[32mOK\033[0m")
            else:
                print("\033[91m" +"2.2 一次開啟多封通知"+ "\033[0m")
            elements = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@class,'NotificationItemRedDot')]"))
            )
            count3 = len(elements)
            sleep(2) 
            element1 = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(@class,"MessageCountBadge")]')))
            element3 = int(element1.text)  
            if element3 == count3 == element2 - 2:
                print("2.3 已讀功能及未讀數量 \033[32mOK\033[0m")
            else:
                print("\033[91m" +"2.3 已讀通知數量錯誤"+ "\033[0m")
















            sleep(10)
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