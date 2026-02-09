
#延遲幾秒再繼續(四秒)
time.sleep(4)
#---------------------------------------------------------------------------------------------------------------------------------------------
#執行裝置返回鍵
driver.press_keycode(4)
#---------------------------------------------------------------------------------------------------------------------------------------------
#點擊功能
driver.find_element(By.ID, package + "titleTextView").click()
#---------------------------------------------------------------------------------------------------------------------------------------------
#輸入欄位清空功能
driver.find_element(By.ID, package + "titleTextView").clear()
#---------------------------------------------------------------------------------------------------------------------------------------------
#輸入值功能
driver.find_element(By.ID, package + "otpCodeEditText").send_keys("123456")
#---------------------------------------------------------------------------------------------------------------------------------------------
#滑動頁面功能
x1, y1 = 348, 1110   ## 起始位置
x2, y2 = 348, 155    ## 終點位置
action = TouchAction(driver)
action.press(x=x1, y=y1).wait(1000).move_to(x=x2, y=y2).release().perform()
##多次點擊(五次)
x1, y1 = 348, 1110   ## 起始位置
x2, y2 = 348, 155    ## 終點位置
action = TouchAction(driver)
for _ in range(5):
	action.press(x=x1, y=y1).wait(1000).move_to(x=x2, y=y2).release().perform()
#---------------------------------------------------------------------------------------------------------------------------------------------
#檢查元素中是否有特定的text值
element1 = driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.TextView")
text1 = element1.text
##文案內容
expected_text = 'There_are_no_orders_currently'
##檢查並印出訊息
if text1 == expected_text:
    print("4.1 Overdue頁面顯示: \033[32mOK\033[0m", expected_text)
else:
    print("\033[91m" +"Overdue頁面顯示錯誤"+ "\033[0m")
#---------------------------------------------------------------------------------------------------------------------------------------------
## 删除文本中的前导和尾随空格
if text.strip() == expected_text.strip():
    print("7.4 三星評分跳轉email內容 \033[32mOK\033[0m")
else:
    print("\033[91m" +"三星評分失效"+ "\033[0m")

#---------------------------------------------------------------------------------------------------------------------------------------------
#檢查元素中enabled為true or false
element = driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.widget.Button")
## 检查元素是否启用
if element.is_enabled():
    print("\033[91m" +"選填欄填寫欄皆空白 可點擊confirm"+ "\033[0m")
else:
    print("5.2.1 選填欄填寫欄皆空白 不得點擊confirm \033[32mOK\033[0m")
#---------------------------------------------------------------------------------------------------------------------------------------------  
# 最大等待執行時間
    wait = WebDriverWait(driver, 10)
    result_element = wait.until(EC.presence_of_element_located((By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.EditText"))) 
#---------------------------------------------------------------------------------------------------------------------------------------------  
#除去text中的空白格
element = driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.widget.Button")
text = element.text
original_string = text
result_string = text.replace(" ", "")
#---------------------------------------------------------------------------------------------------------------------------------------------  
#產生隱碼(第4~8馬是隱碼)
phone_no1 = "9999999110"
masked_number = phone_no1[:3] + "*" * 5 + phone_no1[-2:]
print (masked_number)
#---------------------------------------------------------------------------------------------------------------------------------------------  
#長按功能
element = driver.find_element(By.XPATH, "//android.widget.TextView[@content-desc='Stream IND']")
action.long_press(element).perform()
action.wait(2000).perform() 
#---------------------------------------------------------------------------------------------------------------------------------------------
# 若元素不存在則通過
try:
        element2 = driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.widget.ScrollView/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[3]/android.widget.TextView")
        # 如果找到了元素，可以输出错误信息或执行其他操作
        print("\033[91m" +"Contact 2的Phone Number欄位格式(>20碼) 可超過20碼"+ "\033[0m" )         
except NoSuchElementException:
        # 如果捕获到 NoSuchElementException 异常，说明元素也不存在，一切正常
        print("4.3.3 Phone Number欄位格式(>20碼) 最多20碼 \033[32mOK\033[0m")
#---------------------------------------------------------------------------------------------------------------------------------------------         
# 元素text中包含某個特定文字(Get_my_limit)
element = driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.LinearLayout/android.widget.TextView[2]")
element_text = element.text
if Get_my_limit in element_text:
    print("未認證綁卡頁無綁卡，文案正確:\033[32mOK\033[0m", element_text)
else:
    print("未認證綁卡頁錯誤")
#---------------------------------------------------------------------------------------------------------------------------------------------         
# 只判斷text中的數字部分
element1 = driver.find_element(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.widget.TextView[1]")
text1 = element1.text
## 使用正则表达式提取文本中的数字
pattern = r'\d+'  # 匹配一个或多个数字
numbers1 = re.findall(pattern, text1)
if '1000' in numbers1:
    print("文案中包含数字1000：\033[32mOK\033[0m", numbers1)
else:
    print("\033[91m" + "優惠金額與footer不一致" + "\033[0m")
#---------------------------------------------------------------------------------------------------------------------------------------------
# 拉霸拖曳
slider_element = driver.find_element(By.ID, package +"amountSeekBar")
# 获取拉霸元素的坐标
slider_location = slider_element.location
slider_x = slider_location['x']
slider_y = slider_location['y']
# 指定拉霸的起始位置和结束位置
start_x = slider_x  # 起始位置 x 坐标
end_x = slider_x +400  # 结束位置 x 坐标 (这里根据具体情况调整)
# 执行拖拽操作，模拟滑动拉霸
action.press(x=start_x, y=slider_y).wait(200).move_to(x=end_x, y=slider_y).release().perform()
#---------------------------------------------------------------------------------------------------------------------------------------------
# 點擊座標(X,Y)
action = TouchAction(driver)
# 定义要点击的坐标 (x, y)，这里请替换成你要点击的坐标
x_coordinate = 438
y_coordinate = 1364
# 在指定坐标处执行点击操作
action.tap(x=x_coordinate, y=y_coordinate).perform()
#---------------------------------------------------------------------------------------------------------------------------------------------
# INI中帶變數
email=config.get('customer_email','email')
# 定义变量(email)
app_variable = app_INDEV
name_variable = 'Guest'
phone_variable = phone_no
# 使用字符串替换来填充变量(email)
email = email.replace('${AppVariable}', app_variable)
email = email.replace('${NameVariable}', name_variable)
email = email.replace('${PhoneVariable}', phone_variable)
#---------------------------------------------------------------------------------------------------------------------------------------------
# 尋找頁面文字
page_text = driver.page_source  # 获取页面源代码
search_text = "phone_no"

if search_text in page_text:
    print("找到匹配的文字:", search_text)
else:
    print("未找到匹配的文字")
#---------------------------------------------------------------------------------------------------------------------------------------------
# 點擊特定文字
element = driver.find_element(By.XPATH, "//*[contains(@text, 'Get my limit')]")
element.click()
#---------------------------------------------------------------------------------------------------------------------------------------------
# 計算特定條件的元素數量
elements = driver.find_elements(By.XPATH, "//*[@clickable='true']")
count = len(elements)
print("符合条件的元素数量:", count)
#---------------------------------------------------------------------------------------------------------------------------------------------
# 特定條件的元素點擊(排序)
elements = driver.find_elements(By.XPATH, "//*[@clickable='true']")
if elements:
    elements[2].click()
#---------------------------------------------------------------------------------------------------------------------------------------------
# 清空所有輸入、選填欄位
text_fields = driver.find_elements(By.CLASS_NAME, 'android.widget.EditText')
# 遍历并清空每个文本字段
for field in text_fields:
    field.clear()