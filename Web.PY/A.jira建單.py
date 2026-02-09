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
template = config.get('IN','planform')
################確認國家模板(請輸入 'IN'PK'MEX'PHL'EMI' )###########################

# 启动 Chromedriver
driver = webdriver.Chrome()
################新安卓單(請輸入)###########################
url = "http://jira.he-x-tech.com:8080/browse/APP-2379"
################新安卓單(請輸入)###########################

driver.get(url)
WebDriverWait(driver, 10)

#帳號
driver.find_element(By.CSS_SELECTOR, "#login-form-username").send_keys("lewis")
#密碼
driver.find_element(By.CSS_SELECTOR, "#login-form-password").send_keys("1qaz234%")
#登入
driver.find_element(By.XPATH, "//*[contains(@value, '登录')]").click()
#獲取title
element1 = driver.find_element(By.CSS_SELECTOR, "#summary-val")
text1 = element1.text
# 删除 '[新包]' 并在删除后的文本前添加 '[安卓]'
text_without_new = text1.replace("[新包]", "")
new_title = "[安卓]" + text_without_new

#獲取jira單號
element1 = driver.find_element(By.CSS_SELECTOR, ".issue-link")
text1 = element1.text

# 打开模板网页
driver.get(template)
WebDriverWait(driver, 10)

#更多(複製)
driver.find_element(By.CSS_SELECTOR, ".dropdown-text").click()

element_to_click = driver.find_element(By.XPATH, '//span[text()="复制"]')
element_to_click.click()
# 显式等待，等待元素可见
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input#summary.text.long-field')))
# 输入title
element.send_keys("rogertest2"+new_title)
driver.find_element(By.CSS_SELECTOR, "#clone-issue-submit").click()
sleep(10)
#問題鏈接
driver.find_element(By.CSS_SELECTOR, '#add-links-link').click()
sleep(2)
#輸入安卓單
split_url = url.split("/")
安卓單號 = split_url[-1]
driver.find_element(By.CSS_SELECTOR, '.remote-jira-search-trigger').click()
driver.find_element(By.CSS_SELECTOR, '#link-search-text').send_keys(安卓單號)
driver.find_element(By.CSS_SELECTOR, '#simple-search-panel-button').click()
sleep(1)
driver.find_element(By.XPATH, '//input[@type="checkbox"]').click()
driver.find_element(By.CSS_SELECTOR, '#linkjiraissue-add-selected').click()
sleep(1)
#送出
driver.find_element(By.XPATH, "//*[contains(@value, '链接')]").click()
sleep(10)
driver.quit()
