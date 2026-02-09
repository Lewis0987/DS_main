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
#-------------------------1.提現
        try:
            print("\033[43m\033[30m" + "1.提現" + "\033[0m")
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
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//img[@alt= "add"]'))
            ).click()
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[text()= "Retirar"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//input[contains(@placeholder, "Retirada mínima R$0")]'))
                )
                print("1.1 成功跳轉提現頁\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.1 跳轉提現頁失敗"+ "\033[0m")
#1.2 金額欄位------------------------------------------
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Insira o nome do titular do cartão"]'))
            ).send_keys('asdsdf')
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Insira o seu código CPF"]'))
            ).send_keys('34567777665')
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Por favor insira seu CPF"]'))
            ).send_keys('34567777665')
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Retirar"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()= "Erro de formato"]'))
                )
                print("1.2.1 金額欄位空白(右上)錯誤訊息\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.2.1 金額欄位空白未顯示(右上)錯誤訊息"+ "\033[0m")
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Valor da retirada")]'))
                )
                print("1.2.2 金額欄位空白(欄位)錯誤訊息\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.2.2 金額欄位空白未顯示(欄位)錯誤訊息"+ "\033[0m")

            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Retirada mínima R$0"]'))
            ).send_keys('11')
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "O valor que pode ser sacado")]'))
                )
                print("1.2.3 金額欄位非10倍數(欄位)錯誤訊息\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.2.3 金額欄位非10倍數(欄位)未顯示錯誤訊息"+ "\033[0m")
#1.3 姓名欄位------------------------------------------
            driver.refresh()
            sleep(1)
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Retirada mínima R$0"]'))
            ).send_keys('50')
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Insira o seu código CPF"]'))
            ).send_keys('34567777665')
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Por favor insira seu CPF"]'))
            ).send_keys('34567777665')
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Retirar"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Insira o nome do titular do cartão")]'))
                )
                print("1.3.1 姓名欄位空白(欄位)錯誤訊息\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.3.1 姓名欄位空白(欄位)未顯示錯誤訊息"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Insira o nome do titular do cartão"]'))
            ).send_keys('    ')
            sleep(1)
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Retirar"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Insira o nome do titular do cartão")]'))
                    )
                print("1.3.2 姓名欄位輸入空白格(欄位)錯誤訊息\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.3.2 姓名欄位輸入空白格(欄位)未顯示錯誤訊息"+ "\033[0m")
#1.4 Código CPF空白------------------------------------------
            driver.refresh()
            sleep(1)
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Retirada mínima R$0"]'))
            ).send_keys('50')
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Insira o nome do titular do cartão"]'))
            ).send_keys('esfrs')
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Por favor insira seu CPF"]'))
            ).send_keys('34567777665')
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Retirar"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Informe o CPF no formato correto")]'))
                )
                print("1.4.1 Código CPF空白(欄位)錯誤訊息\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.4.1 Código CPF空白(欄位)未顯示錯誤訊息"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Insira o seu código CPF"]'))
            ).send_keys('1111111111')
            sleep(1)
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Retirar"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Informe o CPF no formato correto")]'))
                    )
                print("1.4.2 Código CPF 10位數(欄位)錯誤訊息\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.4.2 Código CPF 10位數(欄位)未顯示錯誤訊息"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Insira o seu código CPF"]'))
            ).send_keys('9')
            sleep(1)
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Retirar"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Informe o CPF no formato correto")]'))
                    )
                print("\033[91m" +"1.4.3 Código CPF 11位數(欄位)顯示錯誤訊息"+ "\033[0m")
            except TimeoutException:
                print("1.4.3 Código CPF 11位數(欄位)不顯示錯誤訊息\033[32mOK\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Insira o seu código CPF"]'))
            ).send_keys('1')
            sleep(1)
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Retirar"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Informe o CPF no formato correto")]'))
                    )
                print("1.4.4 Código CPF 12位數(欄位)錯誤訊息\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.4.4 Código CPF 12位數(欄位)未顯示錯誤訊息"+ "\033[0m")
#1.5 Tipo Pix選單-------------------------------------------
            def click_option(driver, option_text, option_number):
                button = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "ValueContainer")]'))
                ).click()

                button = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, f"//div[contains(@id, 'react-select-2-listbox')]//*[contains(text(), '{option_text}')]"))
                ).click()

                try:
                    div_element = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, f'//label[contains(text(), "{option_text}")]'))
                    )
                    print(f"1.5.{option_number} Tipo Pix選單{option_text} \033[32mOK\033[0m")
                except TimeoutException:
                    print(f"\033[91m1.5.{option_number} Tipo Pix選單{option_text}錯誤\033[0m")

            # 使用函數簡化代碼
            click_option(driver, 'E-mail', 1)
            click_option(driver, 'CPF', 2)
            click_option(driver, 'Telefone(+55)', 3)
#1.6 CPF--------------------
            driver.refresh()
            sleep(1)
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Retirada mínima R$0"]'))
            ).send_keys('50')
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Insira o nome do titular do cartão"]'))
            ).send_keys('esfrs')
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Insira o seu código CPF"]'))
            ).send_keys('34567777665')
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Retirar"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Informe o CPF no formato correto")]'))
                )
                print("1.6.1 CPF空白(欄位)錯誤訊息\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.6.1 CPF空白(欄位)未顯示錯誤訊息"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Por favor insira seu CPF"]'))
            ).send_keys('1111111111')
            sleep(1)
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Retirar"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Informe o CPF no formato correto")]'))
                    )
                print("1.6.2 CPF 10位數(欄位)錯誤訊息\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.6.2 CPF 10位數(欄位)未顯示錯誤訊息"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Por favor insira seu CPF"]'))
            ).send_keys('9')
            sleep(1)
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Retirar"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Informe o CPF no formato correto")]'))
                    )
                print("\033[91m" +"1.6.3 CPF 11位數(欄位)顯示錯誤訊息"+ "\033[0m")
            except TimeoutException:
                print("1.6.3 CPF 11位數(欄位)不顯示錯誤訊息\033[32mOK\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Por favor insira seu CPF"]'))
            ).send_keys('1')
            sleep(1)
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Retirar"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Informe o CPF no formato correto")]'))
                    )
                print("1.6.4 CPF 12位數(欄位)錯誤訊息\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.6.4 CPF 12位數(欄位)未顯示錯誤訊息"+ "\033[0m")            
#1.7 E-mail--------------------
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "ValueContainer")]'))
            ).click()
            button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@id, 'react-select-2-listbox')]//*[contains(text(), 'E-mail')]"))
            ).click()
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Retirar"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Por favor insira seu e-mail")]'))
                )
                print("1.7.1 E-mail空白(欄位)錯誤訊息\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.7.1 E-mail空白(欄位)未顯示錯誤訊息"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Por favor insira seu e-mail"]'))
            ).send_keys('@qww.ww')
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Retirar"]'))
            ).click()    
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Informe o Email no formato correto")]'))
                )
                print("1.7.2 E-mail未輸入前綴(欄位)錯誤訊息\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.7.2 E-mail未輸入前綴(欄位)未顯示錯誤訊息"+ "\033[0m")
            driver.refresh()
            sleep(1)
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "ValueContainer")]'))
            ).click()
            button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@id, 'react-select-2-listbox')]//*[contains(text(), 'E-mail')]"))
            ).click()
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Por favor insira seu e-mail"]'))
            ).send_keys('qww') 
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Retirar"]'))
            ).click()   
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Informe o Email no formato correto")]'))
                )
                print("1.7.3 E-mail未輸入@(欄位)錯誤訊息\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.7.3 E-mail未輸入@(欄位)未顯示錯誤訊息"+ "\033[0m")
            
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Por favor insira seu e-mail"]'))
            ).send_keys('@')  
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Retirar"]'))
            ).click()  
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Informe o Email no formato correto")]'))
                )
                print("1.7.4 E-mail沒有後綴(欄位)錯誤訊息\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.7.4 E-mail沒有後綴(欄位)未顯示錯誤訊息"+ "\033[0m") 
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Por favor insira seu e-mail"]'))
            ).send_keys('qqq')    
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Retirar"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Informe o Email no formato correto")]'))
                )
                print("1.7.5 E-mail沒有後段(欄位)錯誤訊息\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.7.5 E-mail沒有後段(欄位)未顯示錯誤訊息"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Por favor insira seu e-mail"]'))
            ).send_keys('.qqq')  
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Retirar"]'))
            ).click()  
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Por favor insira seu e-mail")]'))
                )
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Informe o Email no formato correto")]'))
                )
                print("\033[91m" +"1.7.6 E-mail格式正確(欄位)顯示錯誤訊息"+ "\033[0m")
            except TimeoutException:
                print("1.7.6 E-mail格式正確(欄位)顯示錯誤訊息\033[32mOK\033[0m")
#1.8 Telefone(+55)--------------------

            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "ValueContainer")]'))
            ).click()
            button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@id, 'react-select-2-listbox')]//*[contains(text(), 'Telefone(+55)')]"))
            ).click()  
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Retirar"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Número de celular de 10 ou 11 dígitos")]'))
                )
                print("1.8.1 Telefone(+55)空白(欄位)錯誤訊息\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.8.1 Telefone(+55)空白(欄位)未顯示錯誤訊息"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[text()="+55"]/following-sibling::input[@type="text"]'))
            ).send_keys('111111111')
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Retirar"]'))
            ).click()    
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Número de celular de 10 ou 11 dígitos")]'))
                )
                print("1.8.2 Telefone(+55)9碼(欄位)錯誤訊息\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.8.2 Telefone(+55)9碼(欄位)未顯示錯誤訊息"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[text()="+55"]/following-sibling::input[@type="text"]'))
            ).send_keys('1') 
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Retirar"]'))
            ).click()   
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Número de celular de 10 ou 11 dígitos")]'))
                )
                print("\033[91m" +"1.8.3 Telefone(+55)10碼(欄位)顯示錯誤訊息"+ "\033[0m")
            except TimeoutException:
                print("1.8.3 elefone(+55)10碼(欄位)無錯誤訊息\033[32mOK\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[text()="+55"]/following-sibling::input[@type="text"]'))
            ).send_keys('1')  
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Retirar"]'))
            ).click()  
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Número de celular de 10 ou 11 dígitos")]'))
                )
                print("\033[91m" +"1.8.4 Telefone(+55)11碼(欄位)顯示錯誤訊息"+ "\033[0m")
            except TimeoutException:
                print("1.8.4 elefone(+55)11碼(欄位)無錯誤訊息\033[32mOK\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[text()="+55"]/following-sibling::input[@type="text"]'))
            ).send_keys('1')
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Retirar"]'))
            ).click()    
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Número de celular de 10 ou 11 dígitos")]'))
                )
                print("1.8.5 Telefone(+55)12碼(欄位)錯誤訊息\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.8.5 Telefone(+55)12碼(欄位)未顯示錯誤訊息"+ "\033[0m")
            driver.refresh()
            sleep(1)
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "ValueContainer")]'))
            ).click()
            button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@id, 'react-select-2-listbox')]//*[contains(text(), 'Telefone(+55)')]"))
            ).click()
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[text()="+55"]/following-sibling::input[@type="text"]'))
            ).send_keys('aaaaaaaaaaa')
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Retirar"]'))
            ).click()    
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Número de celular de 10 ou 11 dígitos")]'))
                )
                print("1.8.6 Telefone(+55)非數字(欄位)錯誤訊息\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.8.6 Telefone(+55)非數字(欄位)未顯示錯誤訊息"+ "\033[0m")
#1.9 VIP引導鈕--------------------
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()= "Cheque"]'))
            ).click()  
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Descrição do nível VIP")]'))
                )
                print("1.9 VIP頁跳轉\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.9 VIP頁跳轉失效"+ "\033[0m")
            driver.back()
            sleep(1)
#-------------------------2.1充值提示
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[text()= "Depósito"]'))
            ).click()     
            elements = driver.find_elements(By.XPATH, '//*[@data-icon= "question-circle"]')
            if elements:
                elements[0].click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()= "Uma conta que consiste no valor da recarga, recompensas pela participação em atividades, vitórias e derrotas no jogo, etc."]'))
                )
                print("2.1.1充值提示(左)\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"2.1.1充值提示(左)失敗"+ "\033[0m")
            elements = driver.find_elements(By.XPATH, '//*[@data-icon= "question-circle"]')
            if elements:
                elements[1].click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()= "Uma conta composta por recompensas por convidar amigos e retorno de comissões com base no valor da transação dos usuários convidados. "]'))
                )
                print("2.1.2充值提示(右)\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"2.1.2充值提示(右)失敗"+ "\033[0m")
#-------------------------2.2充值欄位
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@value= "100"]'))
                )
                print("2.2.1 預設金額\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"2.2.1 預設金額錯誤"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//input[@type= "number"]'))
            )
            action_chains = ActionChains(driver)
            action_chains.click(element).send_keys(Keys.BACKSPACE * 3).perform()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()= "Depósito mínimo R$ 20"]'))
                )
                print("2.2.2 充值欄位空白錯誤訊息\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"2.2.2 充值欄位空白未顯示錯誤訊息"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//input[@type= "number"]'))
            ).send_keys('19')
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()= "Depósito mínimo R$ 20"]'))
                )
                print("2.2.3 充值欄位金額小於20錯誤訊息\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"2.2.3 充值欄位金額小於20未顯示錯誤訊息"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//input[@type= "number"]'))
            )
            action_chains = ActionChains(driver)
            action_chains.click(element).send_keys(Keys.BACKSPACE * 3).perform()
            element.send_keys('20')
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()= "Depósito mínimo R$ 20"]'))
                )
                print("\033[91m" +"2.2.4 充值欄位金額等於20顯示錯誤訊息"+ "\033[0m")
            except TimeoutException:
                print("2.2.4 充值欄位金額等於20無錯誤訊息\033[32mOK\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//input[@type= "number"]'))
            )
            action_chains = ActionChains(driver)
            action_chains.click(element).send_keys(Keys.BACKSPACE * 2).perform()
            element.send_keys('99999999')
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()= "Depósito mínimo R$ 20"]'))
                )
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()= "O valor máximo de recarga é 99999999"]'))
                )
                print("\033[91m" +"2.2.5 充值欄位金額等於99999999顯示錯誤訊息"+ "\033[0m")
            except TimeoutException:
                print("2.2.5 充值欄位金額等於99999999無錯誤訊息\033[32mOK\033[0m") 
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//input[@type= "number"]'))
            )
            action_chains = ActionChains(driver)
            action_chains.click(element).send_keys(Keys.BACKSPACE * 8).perform()
            element.send_keys('100000000')
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()= "O valor máximo de recarga é 99999999"]'))
                )
                print("2.2.6 充值欄位金額大於99999999顯示錯誤訊息\033[32mOK\033[0m") 
            except TimeoutException:
                print("\033[91m" +"2.2.6 充值欄位金額大於99999999無錯誤訊息"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//input[@type= "number"]'))
            )
            action_chains = ActionChains(driver)
            action_chains.click(element).send_keys(Keys.BACKSPACE * 9).perform()
            element.send_keys('49')
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "background-add-money")]'))
                )
                print("\033[91m" +"2.2.7 充值欄位金額小於50有充值優惠"+ "\033[0m")
            except TimeoutException:
                print("2.2.7 充值欄位金額小於50無充值優惠\033[32mOK\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//input[@type= "number"]'))
            )
            action_chains = ActionChains(driver)
            action_chains.click(element).send_keys(Keys.BACKSPACE * 2).perform()
            element.send_keys('50')
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "background-add-money")]'))
                )
                print("2.2.8 充值欄位金額等於50有充值優惠\033[32mOK\033[0m") 
            except TimeoutException:
                print("\033[91m" +"2.2.8 充值欄位金額等於50有充值優惠"+ "\033[0m")
            element1 = driver.find_element(By.XPATH, '//*[contains(@class, "background-add-money")]')
            text_value_element1 = element1.text
            match = re.search(r'\d+', text_value_element1)
            if match:
                extracted_number = float(match.group())
                # 判斷是否為 element1 的 20%
                is_20_percent = extracted_number == 0.2 * 50  # 假設 50 是 element1 的值
                # 打印結果
                if is_20_percent:
                    print("2.2.9 首充充值優惠金額正確\033[32mOK\033[0m")
                else:
                    print("\033[91m" +"2.2.9 首充充值優惠金額錯誤"+ "\033[0m")
            else:
                print("\033[91m" +"2.2.9 未找到優惠金額"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//input[@type= "number"]'))
            )
            action_chains = ActionChains(driver)
            action_chains.click(element).send_keys(Keys.BACKSPACE * 3).perform()
            element.send_keys('60')
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "background-add-money")]'))
                )
                print("2.2.10 充值欄位金額大於50有充值優惠\033[32mOK\033[0m") 
            except TimeoutException:
                print("\033[91m" +"2.2.10 充值欄位金額大於50有充值優惠"+ "\033[0m")
            element1 = driver.find_element(By.XPATH, '//*[contains(@class, "background-add-money")]')
            text_value_element1 = element1.text
            match = re.search(r'\d+', text_value_element1)
            if match:
                extracted_number = float(match.group())
                # 判斷是否為 element1 的 20%
                is_20_percent = extracted_number == 0.2 * 60  
                # 打印結果
                if is_20_percent:
                    print("2.2.11 首充充值優惠金額正確\033[32mOK\033[0m")
                else:
                    print("\033[91m" +"2.2.11 首充充值優惠金額錯誤"+ "\033[0m")
            else:
                print("\033[91m" +"2.2.11 未找到優惠金額"+ "\033[0m")
#-------------------------2.3充值金額按鈕
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()= "R$ 40,00"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@value= "40"]'))
                )
                div_element = WebDriverWait(driver, 5).until_not(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "background-add-money")]'))
                )
                print("2.3.1 點擊按鈕帶入金額成功\033[32mOK\033[0m")
                print("2.3.2 按鈕金額小於50，未顯示優惠金額\033[32mOK\033[0m") 
            except TimeoutException:
                print("\033[91m" +"2.3.1 點擊按鈕帶入金額失敗"+ "\033[0m")
                print("\033[91m" +"2.3.2 按鈕金額小於50，顯示優惠金額"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()= "R$ 50,00"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@value= "50"]'))
                )
                div_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "background-add-money")]'))
                )
                print("2.3.3 按鈕金額大於等於50，顯示優惠金額\033[32mOK\033[0m") 
            except TimeoutException:
                print("\033[91m" +"2.3.3 按鈕金額大於等於50，未顯示優惠金額"+ "\033[0m")
            element1 = driver.find_element(By.XPATH, '//*[contains(@class, "background-add-money")]')
            text_value_element1 = element1.text
            match = re.search(r'\d+', text_value_element1)
            if match:
                extracted_number = float(match.group())
                # 判斷是否為 element1 的 20%
                is_20_percent = extracted_number == 0.2 * 50  
                # 打印結果
                if is_20_percent:
                    print("2.3.4 按鈕金額大於等於50，首充優惠\033[32mOK\033[0m")
                else:
                    print("\033[91m" +"2.3.4 按鈕金額大於等於50，首充優惠"+ "\033[0m")
            else:
                print("\033[91m" +"2.3.4 未找到優惠金額"+ "\033[0m")
#-------------------------2.4 充值支付頁
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//span[text()= "Depósito"]'))
            ).click()
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//button[text()= "Copiar Código De Pix"]'))
                        ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="Copiado!"]')))
                print("2.4.1 複製支付碼按鈕 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"2.4.1 複製支付碼按鈕失效"+ "\033[0m")
            try:
                clipboard_content = pyperclip.paste()
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//div[@class="text-white break-all mb-4"]'))
                        )
                element_text = element.text
                if clipboard_content == element_text:
                    print("2.4.2 複製功能 \033[32mOK\033[0m")
                else:
                    print("\033[91m" +"2.4.2 複製功能失效"+ "\033[0m")
            except TimeoutException:
                print("未找到複製網址\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"secondary-assistant") and contains(text(),"R$")]'))
            )
            text_value_element1 = element.text

            # 提取數字部分
            extracted_number = ''.join(filter(str.isdigit, text_value_element1))
            if int(extracted_number) == 50:  
                print("2.4.3 支付頁金額\033[32mOK\033[0m")               
            else:
                print("\033[91m" +"2.4.3 支付頁金額錯誤"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//*[text()= "Ja Pago"]'))
                        ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="Total Da Conta"]')))
                print("2.4.4 Ja Pago鈕 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"2.4.4 Ja Pago鈕失效"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//span[text()= "Depósito"]'))
            ).click()
            sleep(1)
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//span[@aria-label="left"]'))
                        ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="Total Da Conta"]')))
                print("2.4.5 支付返回鍵 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"2.4.5 支付返回鍵失效"+ "\033[0m")
#-------------------------2.5 充提紀錄
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[text()= "Registro"]'))
            ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="Método De Depósito"]')))
                print("2.5.1 跳轉充提紀錄頁 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"2.5.1 跳轉充提紀錄頁失效"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//section[contains(@class,"button-list")]//div[text()= "Retirar"]'))
            ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="Taxa De Retirada"]')))
                print("2.5.2 跳轉提現紀錄 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"2.5.2 跳轉提現紀錄失效"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//section[contains(@class,"button-list")]//div[text()= "Depósito"]'))
            ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="Bônus"]')))
                print("2.5.3 跳轉充值紀錄 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"2.5.3 跳轉充值紀錄失效"+ "\033[0m")
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