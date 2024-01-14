import pymysql

def func_show_table_gui(table_name):

    conn = pymysql.connect(
        host='127.0.0.1',
        user='ToumaKazusa',
        password='lsh20031204',
        port=3306,
        database='school'
    )
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'select * from '+ table_name
    try:
        cursor.execute(sql)
        result = cursor.fetchall()  # 返回所有数据
        # result = cursor.fetchone()  # 返回一行数据
        # result = cursor.fetchmany(length)  # fetchmany(size) 获取查询结果集中指定数量的记录，size默认为1
        for line in result:
            print(line)
    except Exception as e:
        conn.rollback()
        print(e)
    finally:
        return result
        cursor.close()
        conn.close()
