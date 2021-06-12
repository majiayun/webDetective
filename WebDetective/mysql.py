import pymysql


def get_pgheader_size():
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root", password="123456", database="tamperdetection")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 按添加时间的降序排列
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
    db.close()
    return x, y, h, w


def get_menus_size():
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root", password="123456", database="tamperdetection")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    #按添加时间的降序排列
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
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()

    db.close()
    return x, y, h, w

def get_pgheader_hash():
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root", password="123456", database="tamperdetection")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 按添加时间的降序排列
    select_sql = "SELECT * FROM  splitimageinfo WHERE partname='pgheader' ORDER BY addtime DESC"

    try:
        # 执行sql语句
        cursor.execute(select_sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        hash = results[0][6]
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()
    db.close()
    return hash

def get_menus_hash():
    # 打开数据库连接
    db = pymysql.connect(host="localhost", user="root", password="123456", database="tamperdetection")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    #按添加时间的降序排列
    select_sql = "SELECT * FROM  splitimageinfo WHERE partname='menus' ORDER BY addtime DESC"

    try:
        # 执行sql语句
        cursor.execute(select_sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        hash = results[0][6]
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()

    db.close()
    return hash

def insert_resphash_info(name,hash):
    db = pymysql.connect(host="localhost", user="root", password="123456", database="tamperdetection")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    insert_sql = "INSERT INTO respsplitimageinfo(partname,hash) VALUES (%s, %s)"
    data = (name, hash)
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