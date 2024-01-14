import pymysql

def func_insert_total_gui(table_name,values):

    conn = pymysql.connect(
        host='127.0.0.1',
        user='ToumaKazusa',
        password='lsh20031204',
        port=3306,
        database='school'
    )

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    res = 0
    sql_insert = 'insert into '+ table_name +' values ' + ' ( '
    for value in values:
        sql_insert += "'" + value + "',"
    sql_insert = sql_insert[0:-1]  + " );"

    try:
        res = 1
        cursor.execute(sql_insert)
        # 提交之前的操作，如果之前已经执行多次的execute，那么就都进行提交
        conn.commit()

    except Exception as e:

        conn.rollback()
        if str(e)[1:5] == "1062":
            res = 2
            print("注意：您插入的值和表中的项主键相同，本次插入将不会生效")
        elif str(e)[1:5] == "1452":
            res = 4
            print("注意：违反外键约束")
        else:
            res = 3
        print(e)
    finally:
        cursor.close()
        conn.close()
        return res