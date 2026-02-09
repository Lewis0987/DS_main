from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import configparser
from colorama import Fore

config = configparser.ConfigParser()
# 启动 Chromedriver
driver = webdriver.Chrome()
################新安卓單(請輸入)###########################
url = "https://www.natal777bet.com/"
################新安卓單(請輸入)###########################
driver.get(url)
WebDriverWait(driver, 10)
sleep(5)

#[登入/註冊]
#手機號
username_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(@type, 'number')]"))
)
username_field.send_keys("9999999888")
print('1.輸入number \033[32mOK\033[0m')
#密碼
inputotp_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(@type, 'password')]"))
)
inputotp_field.send_keys("1111")
print('2.輸入password \033[32mOK\033[0m')
#登入
enter_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Entrar')]")) #針對button的文字尋找
).click()
print('3.點擊button_Enter \033[32mOK\033[0m')
sleep(1)
#關閉Popup(1)_Convite Recompensa
close_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(@alt, 'Close Icon')]"))
).click()
print('4.關閉彈窗_Convite Recompensa \033[32mOK\033[0m')
sleep(1.5)
#關閉Popup(2)_Equilíbrio insuficiente!
close_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[contains(@alt, 'Close Icon')]"))
).click()
print('5.關閉彈窗_Equilíbrio insuficiente! \033[32mOK\033[0m')
sleep(2)
#點擊refresh icon
try:
    refresh_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//img[contains(@alt, 'refresh')]"))
).click()
    print('6.刷新_Balance \033[32mOK\033[0m')
except TimeoutException as e:
    print("\033[91m" +"6.元素不存在"+ "\033[0m", e)
sleep(0.5)
#循环点击刷新按钮N次
for p in range(3):
    driver.find_element(By.XPATH, "//img[contains(@alt, 'refresh')]").click()
    print(f'7.\033[34mBalance刷新 {p+1}次\033[0m \033[32m\u2713\033[0m') #{p+N}連續次數
sleep(0.5)
#首頁logo
try:
    logomenu = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//img[contains(@alt, 'xxx')]"))
).click()
    print('8.首頁logo \033[32mOK\033[0m')
except TimeoutException as e:
    pass 
sleep(1) 
#--------------------------------------------------
#header_遊戲(Jogos)
try:
    Jogos_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'Header__HeaderButtonText-sc-1kbky4o-2 bGMlmR') and text()='Jogos']"))
).click()
    print('9.點擊header_Jogos \033[32mOK\033[0m')
except TimeoutException as e:
    print("\033[91m" +"9.元素不存在"+ "\033[0m", e)   
#header_遊戲(點擊Jogos_子選單點選Telegrama TG客服)
try:
    Telegramabutton_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//button[text()='Telegrama']"))
).click()
    print('10.導向Telegrama頁 \033[32mOK\033[0m')
except TimeoutException as e:
    print("\033[91m" +"10.元素不存在"+ "\033[0m", e)
sleep(1) 
#header_遊戲(點擊Jogos_子選單點選Sobre nós 關於我們)
try:
    Sobrenósbutton_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//button[text()='Sobre nós']"))
).click()
    print('11.導向Sobre nós頁 \033[32mOK\033[0m')
except TimeoutException as e:
    print('\033[91m" +"11.元素不存在"+ "\033[0m')  
#--------------------------------------------------
#header_活動(Atividade)
Atividade_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'Header__HeaderButtonText-sc-1kbky4o-2 bGMlmR') and text()='Atividade']"))
).click()
print('12.點擊header_Atividade \033[32mOK\033[0m')
#header_活動(Atividades_子選單_點選Check in簽到)
checkin_element =WebDriverWait(driver, 10).until(
   EC.presence_of_element_located((By.XPATH, "//button[text()='Check-in']"))
).click()
print('13.點擊header_Check-in \033[32mOK\033[0m')
#header_活動(Atividades_跳轉Check in簽到)
try:
    checkin_element = WebDriverWait(driver,5).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'font-bold text-xl') and contains(text(), 'Regras de recompensa diária VIP')]"))
        )
    print('14.Check-in頁 \033[32mOK \033[0m')
except TimeoutException as e:
    print('\033[91m14.Check in 跳轉失敗 \033[0m')   
#header_活動(Atividades_子選單_點選Primeiro depósito 首存20%)
checkin_element = WebDriverWait(driver,5).until(
     EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Primeiro depósito')]"))
    ).click()
print('15.點擊header_Primeiro depósito \033[32mOK\033[0m')
#header_活動(Atividades_跳轉Primeiro depósito 首存20%)
try:
   Primeirodepósito = WebDriverWait(driver,5).until(
       EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'text-left w-full mb-1 leading-5 md:leading-7') and contains(text(), 'Detalhes do evento:')]"))
   ).click()
   print('16.跳轉首存20% \033[32mOK\033[0m')
except TimeoutException as e:
   print('\033[91m16.首存20% 跳轉失敗 \033[0m')   
input('Press Enter to exit...') 





