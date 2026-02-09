from selenium import webdriver

# 使用 Chrome 的 WebDriver
browser = webdriver.Chrome()

# 開啟 Google 首頁
browser.get('https://www.google.com/')

# 等待用户输入后关闭浏览器(確保瀏覽器不關閉)
input()
