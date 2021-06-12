from selenium.webdriver.common.action_chains import ActionChains
import requests
from selenium import webdriver
import re
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import time
import os.path
import pymysql
from PIL import Image
import os
import tkinter
import hashlib
from bs4 import BeautifulSoup
from win32.lib import win32con
import win32gui
import win32print
from win32api import GetSystemMetrics

#后期修改为使用json文件读入
# SCREEN_HEIGHT = 1440
# SCREEN_WIDTH = 2160
USERNAME = '操作管理员'
PASSWORD = 'JDZX@08_08_2019&Pd'
LOGIN_URL = "http://127.0.0.1:8000/login/"
LOGIN_BUTTON_LOCATION = '/html/body/div[2]/div/div[2]/div/div[2]/div/form/div[3]/input'
XPATH_LIST = ["/html/body/div[2]/div/div[2]/div[1]",
            "/html/body/div[2]/div/div[2]/div[2]",
            "/html/body/div[2]/div/div[2]/div[3]",
            "/html/body/div[2]/div/div[2]/div[4]",
            "/html/body/div[2]/div/div[2]/div[5]",
            "/html/body/div[2]/div/div[2]/div[6]",
            ]
# 配置浏览器驱动路径
DRIVER_PATH = "D:\common software\Google\Chrome\Application\chromedriver.exe"


#获得缩放后的屏幕分辨率，可能与原始分辨率不同
# def get_screen_size():
#     screen = tkinter.Tk()
#     width = screen.winfo_screenwidth()
#     # 获取当前屏幕的宽
#     height = screen.winfo_screenheight()
#     # 获取当前屏幕的高
#     return height, width

def get_real_resolution():
    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    # 横向分辨率
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    # 纵向分辨率
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return w, h


def get_screen_size():
    """获取缩放后的分辨率"""
    w = GetSystemMetrics(0)
    h = GetSystemMetrics(1)
    return w, h


def save_split_image():
    img_path = os.getcwd() + '\\orig_pictures'
    picturenames = os.listdir(img_path)

    for picturename in picturenames:
        #login图片没有头部和菜单栏，不能用来分割
        if 'login' not in picturename:
            img = Image.open(os.getcwd() + '\\orig_pictures\\' + picturename)
            pgheader_size=get_part_size('pgheader')
            pg_x = pgheader_size[0]
            pg_y = pgheader_size[1]
            pg_h = pgheader_size[2]
            pg_w = pgheader_size[3]
            menus_size=get_part_size('menus')
            me_x = menus_size[0]
            me_y = menus_size[1]
            me_h = menus_size[2]
            me_w = menus_size[3]
            # 开始截取
            pg = img.crop((pg_x, pg_y, pg_x + pg_w, pg_y + pg_h))
            me = img.crop((me_x, me_y, me_x + me_w, me_y + me_h))
            # 保存图片
            pg.save(os.getcwd() + "\\orig_splitimage\\pgheader.png")
            me.save(os.getcwd() + "\\orig_splitimage\\menus.png")
        break

#
# def insert_binary_image(name):
#     image=open(os.getcwd()+name+'.png','wb')
#     print(image)


# def get_pgheader_size():
#     # 打开数据库连接
#     db = pymysql.connect(host="localhost", user="root", password="123456", database="tamperdetection")
#     # 使用cursor()方法获取操作游标
#     cursor = db.cursor()
#     # 按添加时间的降序排列
#     select_sql = "SELECT * FROM  splitimageinfo WHERE partname='pgheader' ORDER BY addtime DESC"
#
#     try:
#         # 执行sql语句
#         cursor.execute(select_sql)
#         # 获取所有记录列表
#         results = cursor.fetchall()
#         x = results[0][2]
#         y = results[0][3]
#         h = results[0][4]
#         w = results[0][5]
#     except Exception as e:
#         print(e)
#         # 发生错误时回滚
#         db.rollback()
#     db.close()
#     return x, y, h, w


def get_part_size(partname):
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root", password="123456", database="tamperdetection")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    #按添加时间的降序排列
    select_sql = "SELECT * FROM  splitimageinfo WHERE partname=%s ORDER BY addtime DESC"
    # data = partname
    try:
        # 执行sql语句
        cursor.execute(select_sql, partname)
        # 获取所有记录列表
        results = cursor.fetchall()
        x = results[0][2]
        y = results[0][3]
        h = results[0][4]
        w = results[0][5]
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()

    db.close()
    return x, y, h, w




def insert_th_info(url_now, te, number, rowcount):
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root", password="123456", database="tamperdetection")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    insert_sql = "INSERT INTO thinfo(url,text,numbe,rowcount) VALUES (%s, %s, %s, %s)"
    data = (url_now, te, number, rowcount)
    try:
        # 执行sql语句
        cursor.execute(insert_sql, data)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()
    db.close()


def insert_table_info(url_now, lo_x, lo_y, height, width):
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root", password="123456", database="tamperdetection")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    insert_sql = "INSERT INTO tableinfo(url,location_x, location_y, width,height) VALUES (%s, %s, %s, %s, %s )"
    data = (url_now, lo_x, lo_y, width, height)
    try:
        # 执行sql语句
        cursor.execute(insert_sql, data)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()
    db.close()


def insert_pgheader_info():
    image_pg = open(os.getcwd() + '\\orig_splitimage\\pgheader.png', 'rb')
    # 图片的二进制数据
    pg_data = image_pg.read()
    pg_hash = hashlib.md5(pg_data).hexdigest()
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root", password="123456", database="tamperdetection")

    for pgheader in driver.find_elements_by_class_name("pg-header"):

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        insert_sql = "INSERT INTO splitimageinfo(partname,location_x, location_y,width,height,hash) VALUES (%s, %s, %s, %s, %s, %s )"
        data = ("pgheader", pgheader.location["x"], pgheader.location["y"], pgheader.size["width"], pgheader.size["height"], pg_hash)
        try:
            # 执行sql语句
            cursor.execute(insert_sql, data)
            # 提交到数据库执行
            db.commit()
        except Exception as e:
            print(e)
            # 发生错误时回滚
            db.rollback()
    db.close()

def insert_menus_info():
    image_me = open(os.getcwd() + '\\orig_splitimage\\menus.png', 'rb')
    # 图片的二进制数据
    me_data = image_me.read()
    me_hash = hashlib.md5(me_data).hexdigest()
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root", password="123456", database="tamperdetection")

    for menus in driver.find_elements_by_class_name("menus"):

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        insert_sql = "INSERT INTO splitimageinfo(partname,location_x, location_y,width,height,hash) VALUES (%s, %s, %s, %s, %s, %s)"
        data = ("menus", menus.location["x"], menus.location["y"], menus.size["width"], menus.size["height"], me_hash)
        try:
            # 执行sql语句
            cursor.execute(insert_sql, data)
            # 提交到数据库执行
            db.commit()
        except Exception as e:
            print(e)
            # 发生错误时回滚
            db.rollback()
    db.close()

# def insert_pgheader_info():
#     for pgheader in driver.find_elements_by_class_name("pg-header"):
#         # 打开数据库连接
#         db = pymysql.connect(host="localhost", user="root", password="123456", database="tamperdetection")
#         # 使用cursor()方法获取操作游标
#         cursor = db.cursor()
#         insert_sql = "INSERT INTO pgheaderinfo(url,location_x, location_y,height,width) VALUES (%s, %s, %s, %s, %s )"
#         data = ("pgheader", pgheader.location["x"], pgheader.location["y"], pgheader.size["height"], pgheader.size["width"])
#         try:
#             # 执行sql语句
#             cursor.execute(insert_sql, data)
#             # 提交到数据库执行
#             db.commit()
#             # cursor.execute("select * from tableinfo")
#             # # 查看表里所有数据
#             # data = cursor.fetchall()
#             # print(data)
#         except Exception as e:
#             print(e)
#             # 发生错误时回滚
#             db.rollback()
#         db.close()
#
#
#
# def insert_menus_info(url_now,lo_x,lo_y,height,width):
#     # 打开数据库连接
#     db = pymysql.connect(host="localhost", user="root", password="123456", database="tamperdetection")
#     # 使用cursor()方法获取操作游标
#     cursor = db.cursor()
#     insert_sql = "INSERT INTO menusinfo(url,location_x, location_y,height,width) VALUES (%s, %s, %s, %s, %s )"
#     data = (url_now, lo_x, lo_y, height, width)
#     try:
#         # 执行sql语句
#         cursor.execute(insert_sql,data)
#         # 提交到数据库执行
#         db.commit()
#         # cursor.execute("select * from tableinfo")
#         # # 查看表里所有数据
#         # data = cursor.fetchall()
#         # print(data)
#     except Exception as e:
#         print(e)
#         # 发生错误时回滚
#         db.rollback()
#     db.close()

def save_th_info():
    # 获取整个table中的内容，可能有多个table标签
    tables = driver.find_elements_by_tag_name("table")
    # 获取th的行数
    k = 0
    rowcount = 0
    for i in range(0, len(tables)):
        rowcount = rowcount + len(tables[i].find_elements_by_tag_name('th'))
    for i in range(0, len(tables)):
        for j in range(0, len(tables[i].find_elements_by_tag_name('th'))):
            text = tables[i].find_elements_by_tag_name('th')[j].text
            k = k + 1
            insert_th_info(driver.current_url, text, k, rowcount)


def insert_html_part_info(hn,c,pg,m,co,t,pa,st):
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root", password="123456", database="tamperdetection")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    insert_sql = "INSERT INTO partinfo(htmlname,complete,pgheader,menus,content,ttable,pagination,staticpart) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    data = (hn, c, pg, m, co, t, pa, st)
    try:
        # 执行sql语句
        cursor.execute(insert_sql, data)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()
    db.close()


def save_html_part_info():
    htmlnames = os.listdir(os.getcwd() + '\\orig_htmls')
    for htmlname in htmlnames:
        # login.html不用做区域划分，可以忽略
        if 'login' not in htmlname:
            # 读入html文件
            # path = os.getcwd() + '\\htmls' + htmlname
            file = open(os.getcwd() + '\\orig_htmls\\' + htmlname, 'r', encoding='utf-8')
            html_string = file.read()
            file.close()
            soup = BeautifulSoup(html_string, 'html.parser')
            prety = soup.prettify() #处理好缩进，结构化显示
            # 筛选标签为div且属性class为pg-header的源码
            pgheader_div = soup.find(name="div", attrs={"class": "pg-header"})
            menus_div = soup.find(name="div", attrs={"class": "menus"})
            content_div = soup.find(name="div", attrs={"class": "content"})
            table_div = soup.find(name="table")
            pagination_div = soup.find(name="div", attrs={"class": "col-md-12 text-right"})
            staticpart=str(content_div).replace(str(table_div),'').replace(str(pagination_div),'')

            # if pgheader_div:
            #     # 造出hash工厂
            #     pghash = hashlib.md5(str(pgheader_div).encode("utf-8")).hexdigest()  # hashlib.sha512 ：可以选择不同的算法加密，不同的算法的加密结果的长度也会不一样
            #
            # if menus_div:
            #     # 造出hash工厂
            #     mhash = hashlib.md5(str(menus_div).encode("utf-8")).hexdigest()  # hashlib.sha512 ：可以选择不同的算法加密，不同的算法的加密结果的长度也会不一样

            insert_html_part_info(htmlname, prety, str(pgheader_div), str(menus_div), str(content_div), str(table_div),
                           str(pagination_div), staticpart)


def save_table_info():
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root", password="123456", database="tamperdetection")
    for table in driver.find_elements_by_tag_name("table"):
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        insert_sql = "INSERT INTO tableinfo(url,location_x, location_y,height,width) VALUES (%s, %s, %s, %s, %s )"
        data = (driver.current_url, table.location["x"], table.location["y"], table.size["height"],
                    table.size["width"])
        try:
            # 执行sql语句
            cursor.execute(insert_sql, data)
            # 提交到数据库执行
            db.commit()
        except Exception as e:
            print(e)
            # 发生错误时回滚
            db.rollback()
    db.close()



# def get_pgheader_info():
#     for pgheader in driver.find_elements_by_class_name("pg-header"):
#         insert_pgheader_info(driver.current_url, pgheader.location["x"], pgheader.location["y"], pgheader.size["height"],
#                     pgheader.size["width"])
#
#
# def get_menus_info():
#     for menus in driver.find_elements_by_class_name("menus"):
#         insert_menus_info(driver.current_url, menus.location["x"], menus.location["y"], menus.size["height"],
#                     menus.size["width"])


def save_orig_img():
    img_path = os.getcwd()+'\\orig_pictures'
    img_name = re.split(r'/', driver.current_url)[3] + time.strftime('-%Y-%m%d-%H%M%S', time.localtime(time.time()))
    img = "%s.png" % os.path.join(img_path, img_name)
    driver.get_screenshot_as_file(img)


def save_orig_html():
    html_path = os.getcwd()+'\\orig_htmls'
    html_name = re.split(r'/', driver.current_url)[3] + time.strftime('-%Y-%m%d-%H%M%S', time.localtime(time.time()))
    with open("%s.html" % os.path.join(html_path, html_name), 'w', encoding='utf-8') as f:
        f.write(driver.page_source)

# def get_part_info():
#     # 获取整个table中的内容，可能有多个table标签
#     staticpart = driver.find_element_by_class_name("pg-header")
#     img_path = os.getcwd() + '\\pictures'
#     img_name = re.split(r'/', driver.current_url)[3] +"-static"+ time.strftime('-%Y-%m%d-%H%M%S', time.localtime(time.time()))
#     img = "%s.png" % os.path.join(img_path, img_name)
#     driver.get_screenshot_as_file(img)
#     print(staticpart)


if __name__ == '__main__':
    # 设置浏览器
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')  # 无头参数
    options.add_argument('--disable-gpu')
    # 启动浏览器
    driver = Chrome(executable_path=DRIVER_PATH, options=options)

    # 登陆页面
    driver.get(LOGIN_URL)
    # 窗口最大化
    driver.maximize_window()
    # 设置截屏整个网页的宽度以及高度
    driver.set_window_size(get_screen_size()[0], get_screen_size()[1])
    save_orig_img()
    save_orig_html()

    # 首页
    # 定位登录页面用户名和密码元素并模拟填入用户名和密码
    driver.find_element_by_name("username").send_keys(USERNAME)
    driver.find_element_by_name("password").send_keys(PASSWORD)
    # 模拟点击登录按钮登录
    driver.find_element_by_xpath(LOGIN_BUTTON_LOCATION).click()
    # 首页 保存图片
    save_orig_img()
    save_orig_html()
    insert_pgheader_info()
    insert_menus_info()
    save_split_image()



    # 订单审核
    element = driver.find_element_by_xpath(XPATH_LIST[0])
    ActionChains(driver).move_to_element(element).perform()
    driver.find_elements_by_class_name('btn-primary')[0].click()
    # 保存图片
    # getpartinfo()
    save_orig_img()
    save_orig_html()
    save_table_info()
    save_th_info()


    # 审核数据
    element = driver.find_element_by_xpath(XPATH_LIST[1])
    ActionChains(driver).move_to_element(element).perform()
    driver.find_elements_by_class_name('btn-primary')[1].click()
    # 保存图片
    save_orig_img()
    save_orig_html()
    save_table_info()
    save_th_info()

    # 审核结果
    element = driver.find_element_by_xpath(XPATH_LIST[1])
    ActionChains(driver).move_to_element(element).perform()
    driver.find_elements_by_class_name('btn-primary')[2].click()
    # 保存图片
    save_orig_img()
    save_orig_html()
    save_table_info()
    save_th_info()


    # 分配测试
    element = driver.find_element_by_xpath(XPATH_LIST[2])
    ActionChains(driver).move_to_element(element).perform()
    driver.find_elements_by_class_name('btn-primary')[3].click()
    # 保存图片
    save_orig_img()
    save_orig_html()
    save_table_info()
    save_th_info()

    # 分配结果
    element = driver.find_element_by_xpath(XPATH_LIST[2])
    ActionChains(driver).move_to_element(element).perform()
    driver.find_elements_by_class_name('btn-primary')[4].click()
    # 保存图片
    save_orig_img()
    save_orig_html()
    save_table_info()
    save_th_info()

    # 测试进度
    element = driver.find_element_by_xpath(XPATH_LIST[3])
    ActionChains(driver).move_to_element(element).perform()
    driver.find_elements_by_class_name('btn-primary')[5].click()
    # 保存图片
    save_orig_img()
    save_orig_html()
    save_table_info()
    save_th_info()

    # 测试结果
    element = driver.find_element_by_xpath(XPATH_LIST[3])
    ActionChains(driver).move_to_element(element).perform()
    driver.find_elements_by_class_name('btn-primary')[6].click()
    url = driver.current_url
    # 保存图片
    save_orig_img()
    save_orig_html()
    save_table_info()
    save_th_info()

    # 报表生成
    element = driver.find_element_by_xpath(XPATH_LIST[3])
    ActionChains(driver).move_to_element(element).perform()
    driver.find_elements_by_class_name('btn-primary')[7].click()
    # 保存图片
    save_orig_img()
    save_orig_html()
    save_table_info()
    save_th_info()


    # 分组管理
    element = driver.find_element_by_xpath(XPATH_LIST[4])
    ActionChains(driver).move_to_element(element).perform()
    driver.find_elements_by_class_name('btn-primary')[8].click()
    # 保存图片
    save_orig_img()
    save_orig_html()
    save_table_info()
    save_th_info()


    # 平台监测
    element = driver.find_element_by_xpath(XPATH_LIST[5])
    ActionChains(driver).move_to_element(element).perform()
    driver.find_elements_by_class_name('btn-primary')[9].click()
    # 保存图片
    save_orig_img()
    save_orig_html()
    save_table_info()
    save_th_info()


    # 关闭浏览器
    driver.quit()
    save_html_part_info()


