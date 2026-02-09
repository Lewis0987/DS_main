from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import os
import configparser

config = configparser.ConfigParser()
# 获取当前文件所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
config_keyfile = os.path.join(current_dir, 'jira.ini')
# 讀取配置文件
config.read(config_keyfile, encoding='utf-8')
################確認國家模板(請輸入 'IN'PK'MEX'PHL'EMI')###########################
模板 = config.get('IN','planform')
################確認國家模板(請輸入 'IN'PK'MEX'PHL'EMI' )###########################

# 启动 Chromedriver
driver = webdriver.Chrome()
################新安卓單(請輸入)###########################
url = "http://jira.he-x-tech.com:8080/browse/QA-11201"
################新安卓單(請輸入)###########################

driver.get(url)
WebDriverWait(driver, 10)
#帳號
driver.find_element(By.CSS_SELECTOR, "#login-form-username").send_keys("roger")
#密碼
driver.find_element(By.CSS_SELECTOR, "#login-form-password").send_keys("1qaz234%")
#登入
driver.find_element(By.XPATH, "//*[contains(@value, '登录')]").click()
#主單關閉測試
driver.find_element(By.CSS_SELECTOR, "#action_id_41").click()
driver.find_element(By.CSS_SELECTOR, "#action_id_51").click()
#批量關閉子任務
element_to_click = driver.find_element_by_xpath('//span[text()="选项"]')
element_to_click.click()


sleep(10)