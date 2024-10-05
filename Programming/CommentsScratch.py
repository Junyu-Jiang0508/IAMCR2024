import random
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
import openpyxl
gjz = '南方小土豆'
name_ = '123.xlsx'
workbook = openpyxl.load_workbook(name_)  # 返回一个workbook数据类型的值
sheet = workbook.active     # 获取活动表
hs = sheet.max_row   #最大行数
a = hs+1
had = []
for j in sheet['B']:
    had.append(j.value)

#实例化谷歌设置选项
option = webdriver.ChromeOptions()
#添加保持登录的数据路径：安装目录一般在C:\Users\xujiani\AppData\Local\Google\Chrome\User Data
option.add_argument(r"user-data-dir=C:\Users\didadi\AppData\Local\Google\Chrome\User Data")
#防止滑块验证失败
option.add_argument("--disable-blink-features=AutomationControlled")  # 就是这一行告诉chrome去掉了webdriver痕迹，令navigator.webdriver=false，极其关键

driver = webdriver.Chrome(options=option)
url_=f'https://www.douyin.com/search/{gjz}?aid=225f5441-d66e-47ef-abab-294cffcd2f2b&publish_time=0&sort_type=0&source=search_history&type=general'
#打开网址
driver.get(url_)
input('123')

i = 1
while i==True:
    content = driver.page_source  # 获取当前页元素
    soup = BeautifulSoup(content, 'html.parser')

    for k1 in soup.find_all('div', class_='YkcX1IuK'):
        id = k1.get('id')
        url1 = 'https://www.douyin.com/note/'+id.replace('waterfall_item_', "")

        if url1 in had:
            pass
        else:
            had.append(url1)
            print(url1)
            sheet['G%s' % a] = url1
            sheet['F%s' % a] = gjz
            for k2 in k1.find_all('div', class_='Z6bzLUc0'):
                for k3 in k2.find_all('img'):
                    picture = 'https:'+k3.get('src')#https://p3-pc-sign.douyinpic.com/tos-cn-i-0813/oQn4KANGCuIAg09CAQgdEQfhCAA0Ak76z9AeCs~noop.jpeg?biz_tag=pcweb_cover&from=3213915784&s=PackSourceEnum_SEARCH&se=false&x-expires=1707145200&x-signature=W9kJ%2BnssPRfhsK44IYws%2F1hSaGk%3D
                    # sheet['D%s' % a] = picture
                    print(picture)
            for k3 in k1.find_all('div',class_='di7KBufh'):
                sheet['B%s' % a] = k3.text
                print(k3.text)
            for k3 in k1.find_all('div',class_='r6Ot71mj'):
                sheet['B%s' % a] = k3.text
                # sheet['C%s' % a] = k3.text
                print(k3.text)
            for k3 in k1.find_all('span',class_='i1nSrSLR'):
                sheet['A%s' % a] = k3.text[3:]
                print(k3.text[3:])
            for k3 in k1.find_all('span',class_='fltpsqoh'):
                sheet['A%s' % a] = k3.text[3:]
                print(k3.text[3:])
            a+=1
            workbook.save(name_)  # 保存表格
    input('qwe')
    # # 向下滚动1000个像素
    # driver.execute_script('window.scrollBy(0,1000)')

    # 随机休眠
    # time.sleep(random.uniform(3, 5))

