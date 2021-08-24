import hashlib

from lxml import etree
import os
from PIL import Image
import re
import time


def get_imgs_xpath(filename):
    '''获得当前页面的img标签列表'''
    tree = etree.parse(filename, parser=etree.HTMLParser(encoding="utf-8"))
    # 选取所有的img标签
    res = tree.xpath('//img')
    img_xpath_list = []
    for r in res:
        img_path = r.getroottree().getpath(r)
        img_xpath_list.append(img_path)
    return img_xpath_list


def prepare():
    # 保存源码
    html_path = os.getcwd() + '\\orig_htmls'
    html_name = re.split(r'/', driver.current_url)[3] + time.strftime('-%Y-%m%d-%H%M%S', time.localtime(time.time()))
    html = "%s.html" % os.path.join(html_path, html_name)
    with open(html, 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    # 保存截图
    img_path = os.getcwd() + '\\orig_pictures'
    img_name = re.split(r'/', driver.current_url)[3] + time.strftime('-%Y-%m%d-%H%M%S', time.localtime(time.time()))
    img = "%s.png" % os.path.join(img_path, img_name)
    driver.get_screenshot_as_file(img)
    # 保存img图标和信息
    img_xpath_list = get_imgs_xpath("%s.html" % os.path.join(html_path, html_name))
    save_imgs(img, img_xpath_list)


def save_imgs(picture_name, img_list):
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root", password="123456", database="tamperdetection")
    picture = Image.open(os.getcwd() + '\\orig_pictures\\' + picture_name)
    for img_xpath in img_list:
        res = driver.find_element_by_xpath(img_xpath)
        img_x = res.location["x"]
        img_y = res.location["y"]
        img_w = res.location["width"]
        img_h = res.location["height"]
        # 开始截取
        img = picture.crop((img_x, img_y, img_x + img_w, img_y + img_h))

        # 图像尺寸归一化 其实预处理和检测时是在同一台计算机，截图尺寸应该相等
        # new_img=img.resize((500,500),Image.BILINEAR)
        # new_img=new_img.convert("RGB")
        # 保存图片
        # img.save(os.getcwd() + "\\orig_splitimage\\"+picture_name+img_xpath)
        img_name = os.path.join(os.getcwd(), 'orig_imgs', picture_name, img_xpath, '.png')
        img.save(img_name)
        img_data = open(img_name, 'rb').read()
        img_hash = hashlib.md5(img_data).hexdigest()
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        insert_sql = "INSERT INTO imginfo(partname,location_x, location_y,width,height,hash) VALUES (%s, %s, %s, %s, %s, %s )"
        data = (img_name, img.location["x"], img.location["y"], img.size["width"], img.size["height"], img_hash)
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


