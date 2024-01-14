import pymysql

def func_delete_gui(table_name,limit):

    conn = pymysql.connect(
        host='127.0.0.1',
        user='ToumaKazusa',
        password='lsh20031204',
        port=3306,
        database='school'
    )

    cursor = conn.cursor(pymysql.cursors.DictCursor)

    sql_select = 'select * from ' + table_name +' where ' + limit + ";"
    sql_delete = 'delete from '+ table_name +' where ' + limit + ";"
    res = ""
    try:
        cursor.execute(sql_select)
        result = cursor.fetchall()
        if len(result) > 0:
            print("找到 "+str(len(result))+" 条符合条件数据，已全部删除")
            res = ("找到 "+str(len(result))+" 条符合条件数据，已全部删除")
        if len(result) == 0:
            #不存在时提示，我这里不会有空值的
            print("注意：未找到符合条件数据，本次不删除任何数据，请检查limit")
            res = ("注意：未找到符合条件数据，本次不删除任何数据，请检查limit")
        i = 0
        for line in result:
            i = i + 1
            if i ==5 :
                break
            print(line)
        cursor.execute(sql_delete)
        conn.commit()

    except Exception as e:
        res = "error"
        conn.rollback()
        print(e)
    finally:
        return res,result
        cursor.close()
        conn.close()