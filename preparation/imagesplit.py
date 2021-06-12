# -*- coding: utf-8 -*-
import hashlib

import pymysql
from PIL import Image
import os
import tkinter

def get_pgheader_size():
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root", password="123456", database="tamperdetection")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    select_sql = "SELECT * FROM  splitimageinfo WHERE partname='pgheader' ORDER BY addtime DESC"

    try:
        # 执行sql语句
        cursor.execute(select_sql)
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
    return x, y,h,w
    db.close()

def get_menus_size():
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root", password="123456", database="tamperdetection")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    select_sql = "SELECT * FROM  splitimageinfo WHERE partname='menus' ORDER BY addtime DESC"

    try:
        # 执行sql语句
        cursor.execute(select_sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        x = results[0][2]
        y = results[0][3]
        h = results[0][4]
        w = results[0][5]
        # for result in results:
        #     x = result[2]
        #     y = result[3]
        #     h = result[4]
        #     w = result[5]
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()
    return x, y, h, w
    db.close()

img_path = os.getcwd() + '\\pictures'
myfilelist = os.listdir(img_path)
print(myfilelist)
for filename in myfilelist:
    if 'login' not in filename:
        img = Image.open(os.getcwd() + '\\pictures\\' + filename)
        # 图片尺寸
        img_size = img.size
        # 开始截取
        pgheader_list = get_pgheader_size()
        pg_x = pgheader_list[0]
        pg_y = pgheader_list[1]
        pg_h = pgheader_list[2]
        pg_w = pgheader_list[3]
        print(type(pg_x))
        menus_list = get_menus_size()
        me_x = menus_list[0]
        me_y = menus_list[1]
        me_h = menus_list[2]
        me_w = menus_list[3]

        region1 = img.crop((pg_x, pg_y, pg_x + pg_w, pg_y + pg_h))
        region2 = img.crop((me_x, me_y, me_x + me_w, me_y + me_h))
        # 保存图片
        region1.save(os.getcwd() +"\\pgheader.png")
        region2.save(os.getcwd() +"\\menus.png")
        break

image_pg = open(os.getcwd()+'\\pgheader.png','rb')
#图片的二进制数据
pg_data = image_pg.read()
pg_hash = hashlib.md5(pg_data).hexdigest()
print(pg_hash)
image_me = open(os.getcwd()+'\\menus.png','rb')
#图片的二进制数据
me_data = image_me.read()
me_hash = hashlib.md5(me_data).hexdigest()
print(me_hash)



