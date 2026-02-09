## test
#@@元素@@
# [#]=>尋找ID   
# [.]=>className
# By.XPATH, "//*[contains(@xx, 'xx')
# input('Press Enter to exit...')   >>>>> 暫停操作
# driver.refresh() 刷新
# driver.back() 返回
# pip install pyperclip
# Tab = 大格向右 ，Shift + Tab = 大格向左
checked = True  # 防止重複執行(如果有迴圈 => for i in range(5):  # 這會跑五次，每次都會進 try 區塊)
#------------------------------ 時間限制	for _ in range(60) 限制秒數	改成 while True 持續跑直到全部觸發
# for _ in range(60): # 有迴圈 , while True 不限時間

# while True:
#-----------------> 【找元素方法】
#抓資料 / 擷取文字內容	【presence_of_element_located】
#等待按鈕可點擊再點下去	【element_to_be_clickable】
#要看元素真的出現在畫面上	【visibility_of_element_located】

#input('Press Enter to exit...') 停留執行 

#=========================================================================================================
#bash
## git checkout main          # 切回 main
## git merge fix-temp-branch # 合併剛剛那個分支
## git branch -d fix-temp-branch # 刪除分支


'''
✅ 方法 1：用 CMD 執行下載安裝程式（半自動）
這是最接近「用命令更新」的方法：
cmd貼上
"curl -o python-installer.exe https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe
start python-installer.exe"
'''