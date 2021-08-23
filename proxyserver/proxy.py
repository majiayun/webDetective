import hashlib
import os
import socket
import re
import time
import traceback
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import tkinter
from WebDetective import mysql
from PIL import Image

# 配置浏览器驱动路径  
DRIVER_PATH = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
USERNAME = '操作管理员'
PASSWORD = 'JDZX@08_08_2019&Pd'
LOGIN_URL = "http://127.0.0.1:8000/login/"
LOGIN_BUTTON_LOCATION = '/html/body/div[2]/div/div[2]/div/div[2]/div/form/div[3]/input'

#获得缩放后的屏幕分辨率，可能与原始分辨率不同
def get_screen_size():
    screen = tkinter.Tk()
    x = screen.winfo_screenwidth()
    # 获取当前屏幕的宽
    y = screen.winfo_screenheight()
    # 获取当前屏幕的高
    return x, y


def split_req_content(string):
    i = 0
    while i < len(string) and string[i:i + 4] != "\r\n\r\n":
        i += 1

    return string[i+4:]

def split_resp_headers(string):
    i = 0
    while i < len(string) and string[i:i + 4] != "\r\n\r\n":
        i += 1

    return string[:i+4]
# def cut_out(a, b, string):
#     results = re.findall(".*%s(.*)%s.*" % (a, b), string)
#     return results


def save_resp_html(url, html):
    html_path = os.getcwd()+'\\resp_htmls'
    html_name = url + time.strftime('-%Y-%m%d-%H%M%S', time.localtime(time.time()))
    ff = "%s.html" % os.path.join(html_path, html_name)
    with open(ff, 'w', encoding='utf-8') as f:
        f.write(html)

def save_resp_img(url):
    img_path = os.getcwd()+'\\resp_pictures'
    img_name = url + time.strftime('-%Y-%m%d-%H%M%S', time.localtime(time.time()))
    img = "%s.png" % os.path.join(img_path, img_name)
    driver.get_screenshot_as_file(img)

def main():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 8080))
    s.listen(100)
    while 1:
        conn, addr = s.accept()
        # print(addr)
        headers = ''
        while 1:
            buf = conn.recv(2048).decode('utf-8')
            headers += buf
            if len(buf) < 2048:
                break

        print(headers)
        headers_first = headers.split('\r\n')[0]
        # headers_last = headers.split('\r\n\r\n')[1]
        # print(headers_last)
        # req_type = headers_first.split(' /')[0]
        # if req_type == 'POST':
        #     post_dic = {}
        #     post_infos = headers_last.split('&')
        #     for post_info in post_infos:
        #         post_dic[post_info.split('=')[0]] = post_info.split('=')[1]
        #
        #     print(post_dic)
        #针对不含参数的get请求或post请求，/前/后包含空格
        url_nopara = headers_first.partition(' /')[-1].rpartition('/ ')[0]
        # 针对包含参数的get请求，/前包含空格
        url = headers_first.partition(' /')[-1].rpartition('/?')[0]
        # url_para=''
        # if req_type == 'GET':
        # 获得包含参数的get请求的完整的url
        url_para = url+'/?'+headers_first.partition('?')[-1].rpartition(' ')[0]
        # print(url_para)
        s1 = socket.socket()
        s1.connect(('127.0.0.1', 8000))
        s1.sendall(headers.encode())

        resp = b''
        while 1:
            try:
                buf = s1.recv(1024*8)
            except socket.timeout as e:
                print(e)
                break

            resp += buf
            if not buf or (buf.startswith(b'WebSocket') and buf.endswith(b'\r\n\r\n')):
                break

        try:
            content = split_req_content(resp.decode('utf-8'))
        except Exception as e:
            print(e)
            pass


        #若截取的url不为空，并且响应包含html内容，则生成html文件
        if url_nopara and len(content) > 0:
            save_resp_html(url_nopara, content)
        elif url and len(content) > 0:
            save_resp_html(url, content)


        # # 设置浏览器
        # options = Options()
        # options.add_argument('--no-sandbox')
        # # options.add_argument('--headless')  # 无头参数
        # options.add_argument('--disable-gpu')
        # # 启动浏览器
        # driver = Chrome(executable_path=DRIVER_PATH, options=options)
        # # 窗口最大化
        # driver.maximize_window()
        # # 设置截屏整个网页的宽度以及高度
        # driver.set_window_size(get_screen_size()[0], get_screen_size()[1])
        if url_nopara:
            URL = 'http://127.0.0.1:8000/'+url_nopara+'/'
            img_name = url_nopara + time.strftime('-%Y-%m%d-%H%M%S', time.localtime(time.time()))
        elif url_para !='/?':
            URL = 'http://127.0.0.1:8000/' + url_para
            img_name = url + time.strftime('-%Y-%m%d-%H%M%S', time.localtime(time.time()))

        driver.get(URL)
        # 保存当前页面截图
        img_path = os.getcwd() + '\\resp_pictures'
        img = "%s.png" % os.path.join(img_path, img_name)
        driver.get_screenshot_as_file(img)

        #不是登录页面，登陆页面之后另做处理
        if url_nopara and url_nopara != 'login':
            image = Image.open(img)
            pgheader_size = mysql.get_pgheader_size()
            pg_x = pgheader_size[0]
            pg_y = pgheader_size[1]
            pg_h = pgheader_size[2]
            pg_w = pgheader_size[3]
            menus_size = mysql.get_menus_size()
            me_x = menus_size[0]
            me_y = menus_size[1]
            me_h = menus_size[2]
            me_w = menus_size[3]
            # 开始截取
            pg = image.crop((pg_x, pg_y, pg_x + pg_w, pg_y + pg_h))
            me = image.crop((me_x, me_y, me_x + me_w, me_y + me_h))
            # 保存图片
            pg.save(os.getcwd() + "\\resp_splitimage\\pgheader.png")
            me.save(os.getcwd() + "\\resp_splitimage\\menus.png")
            image_pg = open(os.getcwd() + '\\resp_splitimage\\pgheader.png', 'rb')
            # 图片的二进制数据
            pg_data = image_pg.read()
            pg_hash = hashlib.md5(pg_data).hexdigest()
            image_me = open(os.getcwd() + '\\resp_splitimage\\menus.png', 'rb')
            # 图片的二进制数据
            me_data = image_me.read()
            me_hash = hashlib.md5(me_data).hexdigest()
            mysql.insert_resphash_info('pgheader', pg_hash)
            mysql.insert_resphash_info('menus', me_hash)
            orig_pg_hash = mysql.get_pgheader_hash()
            orig_me_hash = mysql.get_menus_hash()
            if orig_pg_hash != pg_hash or orig_me_hash != me_hash:
                print('send to', addr, "\n")
                wrong_str = '网页已被篡改，请联系管理员!'
                conn.sendall(split_resp_headers(resp.decode('utf-8')).encode('utf_8')+wrong_str.encode('utf_8'))
                conn.close()
            else:
                print('send to', addr, "\n")
                conn.sendall(resp)
                conn.close()
        else:
            print('send to', addr, "\n")
            conn.sendall(resp)
            conn.close()


# 命令入口
if __name__ == '__main__':
    try:
        # 设置浏览器
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')  # 无头参数
        options.add_argument('--disable-gpu')
        # 启动浏览器
        driver = Chrome(executable_path=DRIVER_PATH, options=options)
        # 窗口最大化
        driver.maximize_window()
        # 设置截屏整个网页的宽度以及高度
        driver.set_window_size(get_screen_size()[0], get_screen_size()[1])
        # 先进行一次登录，保证后续传递的url能顺利登录
        # 定位登录页面用户名和密码元素并模拟填入用户名和密码
        driver.get(LOGIN_URL)
        driver.find_element_by_name("username").send_keys(USERNAME)
        driver.find_element_by_name("password").send_keys(PASSWORD)
        # 模拟点击登录按钮登录
        driver.find_element_by_xpath(LOGIN_BUTTON_LOCATION).click()
        print("start server")
        main()
    except Exception as e:
        print(e)
        driver.quit()
    finally:
        print("end server")
        driver.quit()
