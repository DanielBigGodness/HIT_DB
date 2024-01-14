import pymysql

def func_select_gui(table_name,attrs,limit):

    conn = pymysql.connect(
        host='127.0.0.1',
        user='ToumaKazusa',
        password='lsh20031204',
        port=3306,
        database='school'
    )

    cursor = conn.cursor(pymysql.cursors.DictCursor)


    sql = 'select ' + attrs + ' from '+ table_name +' where ' + limit + ";"

    try:
        cursor.execute(sql)
        result = cursor.fetchall()  # 返回所有数据
        # result = cursor.fetchone()  # 返回一行数据
        # result = cursor.fetchmany(length)  # fetchmany(size) 获取查询结果集中指定数量的记录，size默认为1
        if len(result) > 0:
            print("找到 "+str(len(result))+" 条符合条件数据")
        if len(result) == 0:
            #不存在时提示，我这里不会有空值的
            print("未找到符合条件数据，请检查limit")
        i = 0
        for line in result:
            i = i + 1
            if i ==5 :
                break
            print(line)

    except Exception as e:
        conn.rollback()
        print(e)
    finally:
        return result
        cursor.close()
        conn.close()




def func_select_nest_gui(table_name_a,attrs_a,limit_a,table_name_b,attrs_b,limit_b):

    conn = pymysql.connect(
        host='127.0.0.1',
        user='ToumaKazusa',
        password='lsh20031204',
        port=3306,
        database='school'
    )

    cursor = conn.cursor(pymysql.cursors.DictCursor)


    sql_a = 'select ' + attrs_a + ' from '+ table_name_a +' where ' + limit_a
    sql_b = 'select ' + attrs_b + ' from '+ table_name_b +' where ' + limit_b
    sql = sql_a + " ( " + sql_b + " ) "
    print(sql)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()  # 返回所有数据
        # result = cursor.fetchone()  # 返回一行数据
        # result = cursor.fetchmany(length)  # fetchmany(size) 获取查询结果集中指定数量的记录，size默认为1
        if len(result) > 0:
            print("找到 "+str(len(result))+" 条符合条件数据")
        if len(result) == 0:
            #不存在时提示，我这里不会有空值的
            print("未找到符合条件数据，请检查limit")
        i = 0
        for line in result:
            i = i + 1
            if i ==5 :
                break
            print(line)

    except Exception as e:
        conn.rollback()
        print(e)
    finally:
        return result
        cursor.close()
        conn.close()


def func_select_inner_join_gui(table_a,table_b,attrs,limit,cond):

    conn = pymysql.connect(
        host='127.0.0.1',
        user='ToumaKazusa',
        password='lsh20031204',
        port=3306,
        database='school'
    )

    cursor = conn.cursor(pymysql.cursors.DictCursor)


    sql = 'select ' + attrs + ' from '+ table_a + " JOIN "+ table_b + ' ON (' + cond + ') where ' + limit
    #print(sql)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()  # 返回所有数据
        # result = cursor.fetchone()  # 返回一行数据
        # result = cursor.fetchmany(length)  # fetchmany(size) 获取查询结果集中指定数量的记录，size默认为1
        if len(result) > 0:
            print("找到 "+str(len(result))+" 条符合条件数据")
        if len(result) == 0:
            #不存在时提示，我这里不会有空值的
            print("未找到符合条件数据，请检查limit")
        i = 0
        for line in result:
            i = i + 1
            if i ==5 :
                break
            print(line)

    except Exception as e:
        conn.rollback()
        print(e)
    finally:
        return result
        cursor.close()
        conn.close()

def func_select_group_gui_special():

    conn = pymysql.connect(
        host='127.0.0.1',
        user='ToumaKazusa',
        password='lsh20031204',
        port=3306,
        database='school'
    )
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "select stu_id,COUNT(*) from Choose GROUP BY stu_id HAVING COUNT(*)>1;"
    #print(sql)
    try:
        cursor.execute(sql)
        result = cursor.fetchall()  # 返回所有数据
        # result = cursor.fetchone()  # 返回一行数据
        # result = cursor.fetchmany(length)  # fetchmany(size) 获取查询结果集中指定数量的记录，size默认为1
        if len(result) > 0:
            print("找到 "+str(len(result))+" 条符合条件数据")
        if len(result) == 0:
            #不存在时提示，我这里不会有空值的
            print("未找到符合条件数据，请检查limit")
        i = 0
        for line in result:
            i = i + 1
            if i ==5 :
                break
            print(line)

    except Exception as e:
        conn.rollback()
        print(e)
    finally:
        return result
        cursor.close()
        conn.close()