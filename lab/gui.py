import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic


from show_table_ import func_show_table_gui
from insert_ import func_insert_total_gui
from delete_ import func_delete_gui
from select_ import func_select_gui,func_select_nest_gui,func_select_inner_join_gui,func_select_group_gui_special


'''
添加学生写value  比如  2021112952,liusihao,M,2023-11-18,class001
添加老师写value  比如  teacher020,jinye,school001
删除学生和老师都写limit  比如  name='liusihao'
查询学生和老师写 attrs@limit  比如  class_id@name='stu_jia'

查询学员都有哪些专业(嵌套查询)  写学院名 比如  school_jia
查询挂科学生（连接查询） 不用输入
查询至少选修了两门课的学生(分组查询)  不用输入

以下是三个视图
查询专业major001有哪些人
查询学院school001的老师都开了哪些课
查询班级class001挂科的学生
'''


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.ui = uic.loadUi("./untitled.ui")  # 加载由Qt Designer设计的ui文件
        print(self.ui.__dict__)  # 打印ui文件的属性（如pushButton等）


        self.ui.button_insert_student.clicked.connect(self.insert_student)  # pushButton 绑定onClicked 函数
        self.ui.button_insert_teacher.clicked.connect(self.insert_teacher)
        self.ui.button_delete_student.clicked.connect(self.delete_student)  # pushButton 绑定onClicked 函数
        self.ui.button_delete_teacher.clicked.connect(self.delete_teacher)
        self.ui.button_select_student.clicked.connect(self.select_student)  # pushButton 绑定onClicked 函数
        self.ui.button_select_teacher.clicked.connect(self.select_teacher)
        self.ui.button_all_major.clicked.connect(self.select_all_majors)
        self.ui.button_no_pass.clicked.connect(self.select_no_pass)
        self.ui.button_select_student_up2.clicked.connect(self.select_student_up2)
        self.ui.button_select_major001.clicked.connect(self.select_major001)
        self.ui.button_select_school001.clicked.connect(self.select_school001)
        self.ui.button_select_class001.clicked.connect(self.select_class001)
        self.ui.button_help.clicked.connect(self.help)

        self.ui.button_clear.clicked.connect(self.textBrowser_clear)

    def get_content(self):
        content = self.ui.textEdit.toPlainText()
        return content

    def printf(self, mes):
        self.ui.textBrowser.append(mes)  # 在指定的区域显示提示信息
        self.cursot = self.ui.textBrowser.textCursor()
        self.ui.textBrowser.moveCursor(self.cursot.End)
    def printf_2(self, mes):
        self.ui.textBrowser_2.append(mes)  # 在指定的区域显示提示信息
        self.cursot = self.ui.textBrowser_2.textCursor()
        self.ui.textBrowser_2.moveCursor(self.cursot.End)
    def textBrowser_clear(self):
        self.ui.textBrowser.clear()
    def textBrowser2_clear(self):
        self.ui.textBrowser_2.clear()



    def insert_student(self):

        # 空值约束是用于没写那列的时候，但是我们这里不会有
        content = self.get_content()
        values = content.split(',')

        if len(values)!=5:
            self.printf("value应为5个参数，请看说明")
            return
        for value in values:
            if value=='':
                self.printf("不能有空值")
                return


        res = func_insert_total_gui("Student", values)
        if res == 1:
            self.printf("插入成功")
        if res == 2 :
            self.printf("主键重复，本次插入不生效")
        if res == 3:
            self.printf("其他异常，请查看终端")
        if res == 4:
            self.printf("编号不存在，违反外键约束，本次插入不生效")
        # self.printf(str(res))

    def insert_teacher(self):
        # insert --table coaches --values 2021,shushu,M,2020-10-10,11111111100,游泳
        content = self.get_content()
        values = content.split(',')
        for value in values:
            if value=='':
                self.printf("不能有空值")
        if len(values)!=3:
            self.printf("value应为3个参数，请看说明")
            return
        for value in values[0:-1]:
            if value == '':
                self.printf("不能有空值，本次插入不生效")
                return
        res = func_insert_total_gui("Teacher", values)
        if res == 1:
            self.printf("插入成功")
        if res == 2 :
            self.printf("主键重复，本次插入不生效")
        if res == 3:
            self.printf("其他异常，请查看终端")
        if res == 4:
            self.printf("编号不存在，违反外键约束，本次插入不生效")
        # self.printf(str(res))


    def delete_student(self):

        content = self.get_content()
        limit = content

        res,result = func_delete_gui("Student", limit)
        self.printf(res)
        i = 0
        for line in result:
            i = i + 1
            if i ==11 :
                break
            self.printf(str(line))
        # self.printf(str(res))

    def delete_teacher(self):

        content = self.get_content()
        limit = content

        res,result = func_delete_gui("Teacher", limit)
        self.printf(res)
        i = 0
        for line in result:
            i = i + 1
            if i ==11 :
                break
            self.printf(str(line))
        # self.printf(str(res))

    def select_student(self):
        content = self.get_content()
        values = content.split('@')
        attr = values[0]
        limit = values[1]
        result = func_select_gui("Student",attr,limit)

        if len(result) > 0:
            self.printf("找到 "+str(len(result))+" 条符合条件数据")
        if len(result) == 0:
            #不存在时提示，我这里不会有空值的
            self.printf("未找到符合条件数据，请检查limit")
        i = 0
        for line in result:
            i = i + 1
            if i ==11 :
                break
            self.printf(str(line))

    def select_teacher(self):
        content = self.get_content()
        values = content.split('@')
        attr = values[0]
        limit = values[1]
        result = func_select_gui("Teacher",attr,limit)

        if len(result) > 0:
            self.printf("找到 "+str(len(result))+" 条符合条件数据")
        if len(result) == 0:
            #不存在时提示，我这里不会有空值的
            self.printf("未找到符合条件数据，请检查limit")
        i = 0
        for line in result:
            i = i + 1
            if i ==11 :
                break
            self.printf(str(line))

    def select_all_majors(self):
        content = self.get_content()
        values = content.split(',')

        result = func_select_nest_gui("Major",'*',"school_id=","School",'school_id',"name='"+content+"'")

        if len(result) > 0:
            self.printf("找到 "+str(len(result))+" 条符合条件数据")
        if len(result) == 0:
            #不存在时提示，我这里不会有空值的
            self.printf("未找到符合条件数据，请检查limit")
        i = 0
        for line in result:
            i = i + 1
            if i ==11 :
                break
            self.printf(str(line))


    def select_no_pass(self):
        content = self.get_content()
        values = content.split(',')

        result = func_select_inner_join_gui("Student","Score","*","Score.score_val<60","Student.stu_id=Score.stu_id")

        if len(result) > 0:
            self.printf("找到 "+str(len(result))+" 条符合条件数据")
        if len(result) == 0:
            #不存在时提示，我这里不会有空值的
            self.printf("未找到符合条件数据，请检查limit")
        i = 0
        for line in result:
            i = i + 1
            if i ==11 :
                break
            self.printf(str(line))


    def select_student_up2(self):
        content = self.get_content()
        values = content.split(',')

        result = func_select_group_gui_special()

        if len(result) > 0:
            self.printf("找到 "+str(len(result))+" 条符合条件数据")
        if len(result) == 0:
            #不存在时提示，我这里不会有空值的
            self.printf("未找到符合条件数据，请检查limit")
        i = 0
        for line in result:
            i = i + 1
            if i ==11 :
                break
            self.printf(str(line))

    def select_major001(self):
        result = func_show_table_gui("major001_on_DB")
        if len(result) > 0:
            self.printf("找到 "+str(len(result))+" 条符合条件数据")
        if len(result) == 0:
            #不存在时提示，我这里不会有空值的
            self.printf("未找到符合条件数据，请检查limit")
        i = 0
        for line in result:
            i = i + 1
            if i ==11 :
                break
            self.printf(str(line))
    def select_school001(self):
        result = func_show_table_gui("school001_on_DB")
        if len(result) > 0:
            self.printf("找到 "+str(len(result))+" 条符合条件数据")
        if len(result) == 0:
            #不存在时提示，我这里不会有空值的
            self.printf("未找到符合条件数据，请检查limit")
        i = 0
        for line in result:
            i = i + 1
            if i ==11 :
                break
            self.printf(str(line))
    def select_class001(self):
        result = func_show_table_gui("class001_on_DB")
        if len(result) > 0:
            self.printf("找到 "+str(len(result))+" 条符合条件数据")
        if len(result) == 0:
            #不存在时提示，我这里不会有空值的
            self.printf("未找到符合条件数据，请检查limit")
        i = 0
        for line in result:
            i = i + 1
            if i ==11 :
                break
            self.printf(str(line))

    def help(self):
        self.textBrowser_clear()
        help_str = "添加学生写value  比如  2021112952,liusihao,M,2023-11-18,class001\n添加老师写value  比如  teacher020,lubenwei,school001\n删除学生和老师都写limit  比如  name='liusihao'\n查询学生和老师写 attrs@limit  比如  class_id@name='stu_jia'\n\n查询学员都有哪些专业(嵌套查询)  写学院名 比如  school_jia\n查询挂科学生（连接查询） 不用输入\n查询至少选修了两门课的学生(分组查询)  不用输入\n\n以下是三个视图\n查询专业major001有哪些人\n查询学院school001的老师都开了哪些课\n查询班级class001挂科的学生"
        self.printf(help_str)

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建对象

    w = MyWindow()
    # 展示窗口
    w.ui.show()

    # 程序进行循环等待状态
    app.exec_()