import base64
'''
b = base64.b64decode("hpaB47VL6naC8WmPb75Rxu+FFhskvJbEwjKZqdxkFtM=")
print(len(b), b[:64])
print(b.hex())



print("\033[106m\033[30m" + "A.[登入/註冊]" + "\033[0m")
print("\033[44m\033[32m" + "Subscribe 訂閱" + "\033[0m")
print(f"\033[32m✅ 下載完成：\033[0m")
print(f"\033[31m🗑️ 已刪除：\033[0m")
print(f"\033[33m🗑️ 已刪除：\033[0m")
print('\033[31m背景偵測popup，開始 \033[0m')
print("\033[33m🎉 所有 Banner 都已觸發完成！\033[0m")
'''
lis = [3, 1, 2]
# reverse
lis.reverse() #反向排序
print(lis)  # [2, 1, 3]

lis.sort() #排序大小
print(lis)  # [[1, 2, 3]]


def p(name, age):
    print(f"姓名: {name}, 年齡: {age}")
    return

r = p(age=50, name='Ruby')

class Person:
    def __init__(self, name):
        self.name = name

    def say(self):
        print(f"Hi, I'm {self.name}")

p = Person("Ruby")
p.say()

# 計算
def add(a, b):
    return a + b
print(add (10, 25))   # 總和35




def compound_saving(amount, rate, months):
    if amount > 10_000_000:
        print("本金超過 1000 萬，無法計算。")
        return
    
    monthly_rate = rate / 12
    total = 0.0

    for m in range(1, months + 1):
        total = (total + amount) * (1 + monthly_rate)
        print(f"第 {m} 月：{math.ceil(total)}")
