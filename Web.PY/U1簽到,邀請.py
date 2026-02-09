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
#<<<<<<<<<<<<<<<<<<<<<背景偵測popup，並關閉>>>>>>>>>>>>>>>>>>>>>>
exit_event = threading.Event()
def handle_popups(driver):
    while not exit_event.is_set():
        try:
            # 在这里执行查找弹窗的操作
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Equilíbrio insuficiente!") or contains(text(), "Convide usuários limitados para compartilhar")]'))
            )
            # 找到弹窗后执行关闭的操作
            close_button = driver.find_element(By.CSS_SELECTOR, '[alt="Close Icon"]')
            ActionChains(driver).move_to_element(close_button).click().perform()
            print('关闭一个弹窗成功')

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
        popup_thread = threading.Thread(target=handle_popups, args=(driver,))
        popup_thread.start()
    #-------------------------1.報到
        try:
            print("\033[43m\033[30m" + "1.報到" + "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[type="number"]'))
            ).send_keys('99999990000')
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[type="password"]'))
            ).send_keys('1111')
            button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "ConfirmButton")]'))
            ).click()
            sleep(5)
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Jogos")]'))
            ).click()
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//button[contains(text(), "Check-in")]'))
            ).click()
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[text()="VIP" and text()="2"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "CurrentButton") and .//div[text()="VIP" and text()="2"]]'))
                )
                print("1.1 切換VIP2\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.1 切換VIP2失效"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[text()="VIP" and text()="1"]'))
            ).click()
            try:
                div_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//button[contains(@class, "CurrentButton") and .//div[text()="VIP" and text()="1"]]'))
                )
                print("1.2 切換VIP1\033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.2 換VIP1失效"+ "\033[0m")
            for vip_level in range(3, 26):
                vip_xpath = f'//div[text()="VIP" and text()="{vip_level}"]'
                button_xpath = f'//button[contains(@class, "CurrentButton") and .//div[text()="VIP" and text()="{vip_level}"]]'

                # 切换到相应的 VIP 等级
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, vip_xpath))
                ).click()
                try:
                    # 检查按钮状态
                    div_element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, button_xpath))
                    )
                    print(f"1.{vip_level} 切换VIP{vip_level} \033[32mOK\033[0m")
                except TimeoutException:
                    print(f"\033[91m1.{vip_level} 切换VIP{vip_level}失效\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[text()="Colete cupons"]'))
            ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="O VIP 0 temporariamente não suporta"]')))
                print("1.26 Colete cupons \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.26 Colete cupons失效"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="visualizar registros >"]'))
            ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="Registro Diário de Presença"]')))
                print("1.27 報到紀錄 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.27 報到紀錄失效"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@data-icon="left"]'))
            ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="visualizar registros >"]')))
                print("1.28 報到紀錄返回鍵 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.28 報到紀錄返回鍵失效"+ "\033[0m")
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@data-icon="left"]'))
            ).click()
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[text()="Slots"]')))
                print("1.29 報到返回鍵 \033[32mOK\033[0m")
            except TimeoutException:
                print("\033[91m" +"1.29 報到返回鍵失效"+ "\033[0m")
            print("\033[48;5;22m\033[97m" + "1.報到OK" + "\033[0m")
            print("\033[43m\033[30m" + "2.邀請" + "\033[0m")
        #-------------------------2.邀請(上下級邀請)
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Jogos")]'))
            ).click()
            element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Convidar")]'))
                    ).click()
            sleep(0.5)
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Instruções diárias de recompensa de comissão")]'))
                        )
                action = ActionChains(driver)
                action.click(element).perform()
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Dados diários")]'))
                        ).click()
                try:
                    element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()="Prêmio total"]')))
                    print("2.1.1 邀請紀錄 \033[32mOK\033[0m")
                except TimeoutException:
                    print("\033[91m" +"2.1.1 邀請紀錄失效"+ "\033[0m")
                elements = driver.find_elements(By.XPATH,'//div[contains(text(), "Promoção nível 2")]')     
                if elements:
                    elements[0].click()
                    elements[1].click()
                try:
                    element = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()="Primeira Recarga Recompensas"]')))
                    print("\033[91m" +"2.1.2 每日及總計的二級邀請filter失效"+ "\033[0m")
                except TimeoutException:
                    print("2.1.2 每日及總計的二級邀請filter \033[32mOK\033[0m")
                elements = driver.find_elements(By.XPATH,'//div[contains(text(), "Promoção nível 1")]')     
                if elements:
                    elements[0].click()
                    elements[1].click()
                try:
                    element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()="Primeira Recarga Recompensas"]')))
                    print("2.1.3 每日及總計的一級邀請filter \033[32mOK\033[0m")
                except TimeoutException:
                    print("\033[91m" +"2.1.3 每日及總計的一級邀請filter失效"+ "\033[0m")
                elements = driver.find_elements(By.XPATH,'//div[contains(text(), "Promoção nível 3")]')     
                if elements:
                    elements[0].click()
                    elements[1].click()
                try:
                    element = WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()="Primeira Recarga Recompensas"]')))
                    print("\033[91m" +"2.1.4 每日及總計的三級邀請filter失效"+ "\033[0m")
                except TimeoutException:
                    print("2.1.4 每日及總計的三級邀請filter \033[32mOK\033[0m")
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//*[contains(text(), "Registro")]'))
                        ).click()
                try:
                    element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()="Hora De Entrada"]')))
                    print("2.2.1 反水獎勵紀錄 \033[32mOK\033[0m")
                except TimeoutException:
                    print("\033[91m" +"2.2.1 反水獎勵紀錄失效"+ "\033[0m")
                    element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//div[contains(@style,"padding")]'))
                ).click()
                try:
                    element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.ant-picker.ant-picker-range')))
                    print("2.2.2 日期開啟 \033[32mOK\033[0m")
                except TimeoutException:
                    print("\033[91m" +"2.2.2 日期開啟失效"+ "\033[0m")
                
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//*[text()="Registros de liquidação"]'))
                ).click()
                try:
                    element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "icon-loading")]'))
                    )
                    print("2.2.3 紀錄重整紐\033[32mOK\033[0m")
                except TimeoutException:
                    print("\033[91m" +"2.2.3 紀錄重整紐失效"+ "\033[0m")
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@data-icon="left"]'))
                ).click()
                try:
                    element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()="Instruções diárias de recompensa de comissão"]')))
                    print("2.2.4 反水獎勵返回鍵 \033[32mOK\033[0m")
                except TimeoutException:
                    print("\033[91m" +"2.2.4 反水獎勵返回鍵失效"+ "\033[0m")
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Dados diários")]'))
                        ).click()
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Como convidar")]'))
                        ).click()
                try:
                    element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()="Instruções diárias de recompensa de comissão"]')))
                    print("2.3.1 Como convidar鍵 \033[32mOK\033[0m")
                except TimeoutException:
                    print("\033[91m" +"2.3.1 Como convidar鍵失效"+ "\033[0m")

                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//button[text()= "Cópia"]'))
                        ).click()
                try:
                    element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()="Copiado!"]')))
                    print("2.3.2 複製網址鍵 \033[32mOK\033[0m")
                except TimeoutException:
                    print("\033[91m" +"2.3.2 複製網址鍵失效"+ "\033[0m")
                try:
                    clipboard_content = pyperclip.paste()
                    element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH,'//*[contains(@class,"text-sm sm:text-base")]'))
                            )
                    element_text = element.text
                    print(element_text)
                    print(clipboard_content)
                    if clipboard_content == element_text:
                        print("2.3.3 複製功能 \033[32mOK\033[0m")
                    else:
                        print("\033[91m" +"2.3.3 複製功能失效"+ "\033[0m")
                except TimeoutException:
                    print("未找到複製網址\033[0m")
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@data-icon="left"]'))
                ).click()
                try:
                    element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()="Slots"]')))
                    print("2.3.4 邀請頁返回鍵 \033[32mOK\033[0m")
                except TimeoutException:
                    print("\033[91m" +"2.3.4 邀請頁返回鍵失效"+ "\033[0m")
            except TimeoutException:
                print("\033[44m\033[97m" + "2.無接上邀請" + "\033[0m")
        #-------------------------2.邀請(寶箱)
            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Pessoas de nível inferior eficazes ")]'))
                        )
                action = ActionChains(driver)
                action.click(element).perform()
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//div[contains(text(), ">>>Detalhes")]'))
                        ).click()
                try:
                    element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()="Meus Indicados"]')))
                    print("2.1.1 寶箱紀錄 \033[32mOK\033[0m")
                except TimeoutException:
                    print("\033[91m" +"2.1.1 寶箱紀錄失效"+ "\033[0m")
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//span[text()="Eficiente"]'))
                        ).click()
                try:
                    element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH,'//div[text()="Eficiente"]')))
                    print("2.1.2 紀錄狀態filter(Eficiente) \033[32mOK\033[0m")
                except TimeoutException:
                    print("\033[91m" +"2.1.2 紀錄狀態filter(Eficiente)失效"+ "\033[0m")
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//span[text()="Inválido"]'))
                        ).click()
                try:
                    element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH,'//div[text()="Inválido"]')))
                    print("2.1.2 紀錄狀態filter(Inválido) \033[32mOK\033[0m")
                except TimeoutException:
                    print("\033[91m" +"2.1.2 紀錄狀態filter(Inválido)失效"+ "\033[0m")
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//span[text()="Tudo"]'))
                        ).click()
                try:
                    element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH,'//div[text()="Tudo"]')))
                    print("2.1.3 紀錄狀態filter(Tudo) \033[32mOK\033[0m")
                except TimeoutException:
                    print("\033[91m" +"2.1.3 紀錄狀態filter(Tudo)失效"+ "\033[0m")
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//svg[@data-icon= "close"]'))
                        ).click()
                try:
                    element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH,'//div[contains(text(), "Promoção sujeita ao cumprimento de todas as seguintes condições.")]'))
                        )
                    print("2.1.4 寶箱紀錄X icon功能 \033[32mOK\033[0m")
                except TimeoutException:
                    print("\033[91m" +"2.1.4 寶箱紀錄X icon功能失效"+ "\033[0m")

                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH,'//*[contains(text(), "Cópia")]'))
                        ).click()
                try:
                    element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()="Copiado!"]')))
                    print("2.2.1 複製網址鍵 \033[32mOK\033[0m")
                except TimeoutException:
                    print("\033[91m" +"2.2.1 複製網址鍵失效"+ "\033[0m")
                try:
                    clipboard_content = pyperclip.paste()
                    element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH,'//*[contains(@class,"text-sm sm:text-base")]'))
                            )
                    element_text = element.text
                    print(element_text)
                    print(clipboard_content)
                    if clipboard_content == element_text:
                        print("2.2.2 複製功能 \033[32mOK\033[0m")
                    else:
                        print("\033[91m" +"2.2.2 複製功能失效"+ "\033[0m")
                except TimeoutException:
                    print("未找到複製網址\033[0m")
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@data-icon="left"]'))
                ).click()
                try:
                    element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[text()="Slots"]')))
                    print("2.2.3 邀請頁返回鍵 \033[32mOK\033[0m")
                except TimeoutException:
                    print("\033[91m" +"2.2.3 邀請頁返回鍵失效"+ "\033[0m")
            except TimeoutException:
                print("\033[44m\033[97m" + "2.無接上寶箱" + "\033[0m")
            total_percentage = sys.stdout.total_count / sys.stdout.total_count * 100
            green_percentage = sys.stdout.green_count / sys.stdout.total_count * 100
            red_percentage = sys.stdout.red_count / sys.stdout.total_count * 100
            print("測試項目"+ "\033[93m"f"{ui_version}{product}"+"\033[0m")
            print(f"總測試筆數: {sys.stdout.total_count} ({total_percentage:.2f}%)")
            print(f"\033[32m測試成功筆數: {sys.stdout.green_count} ({green_percentage:.2f}%)\033[0m")
            print(f"\033[91m測試失敗筆數: {sys.stdout.red_count} ({red_percentage:.2f}%)\033[0m")
        except TimeoutException:
            # 超时异常，表示未找到弹窗，不输出错误信息
            pass

        finally:
            
            exit_event.set()
            
        # 关闭 WebDriver
            
        # 等待弹窗处理线程结束
            popup_thread.join() 
if __name__ == "__main__":
    main()