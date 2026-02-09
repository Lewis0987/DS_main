from appium import webdriver
import time

# Appium Server 連線位址
server_url = "http://127.0.0.1:4723/wd/hub"

# 測試裝置與 App 設定 (Desired Capabilities)
desired_caps = {
    "platformName": "Android",
    "platformVersion": "12",          # 你的裝置 Android 版本
    "deviceName": "emulator-5554",    # adb devices 查到的名稱
    "automationName": "UiAutomator2",
    "appPackage": "com.android.calculator2",   # 計算機 App 的 package
    "appActivity": ".Calculator",             # 主 Activity
    "noReset": True
}

# 建立連線
driver = webdriver.Remote(server_url, desired_caps)

# 等幾秒讓 App 開起來
time.sleep(3)

# 找一個按鈕 (例如數字 5) 並點擊
button_5 = driver.find_element("id", "com.android.calculator2:id/digit_5")
button_5.click()

time.sleep(2)

# 關閉 Session
driver.quit()
