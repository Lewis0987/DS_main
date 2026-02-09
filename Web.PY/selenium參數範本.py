#@@元素@@
#[#]=>尋找ID   
#[.]=>className
#By.XPATH, "//*[contains(@xx, 'xx')
#暫停操作 input('Press Enter to exit...') 
#driver.refresh()
#driver.back()
#pip install pyperclip

#========================================================================================================
try:
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"Balanço Total")]'))
    )
    print("8.2引導至儲值頁\033[32mOK\033[0m")
except TimeoutException:
    print("\033[91m" +"8.2 引導至儲值頁失敗"+ "\033[0m")

#========================================================================================================  
# 循环点击刷新按钮N次
for _ in range(1000):
    driver.find_element(By.XPATH, "//img[contains(@alt, 'refresh')]").click()
sleep(60)
print('7.連續刷新_Balance \033[32mOK\033[0m')

#========================================================================================================
#尋找較焦距元素
element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "ImageTab")]//span[text()= "Cards"]'))
        ).click()


#========================================================================================================
target_element = driver.find_element(By.XPATH,'//*[contains(text(), "A partir de agora,")]')
 # 使用 ActionChains 模拟鼠标点击
action = ActionChains(driver)
action.click(target_element).perform()
