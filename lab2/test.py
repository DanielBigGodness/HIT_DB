# coding=utf-8
import treePlotter
from util import util
query1="SELECT [ ENAME = ' Mary ' & DNAME = ' Reserach '] ( ( EMPLOYEE ) JOIN ( DEPARTMENT ) )"
query2="PROJECTION [ BDATE ] ( SELECT [ ENAME = John & DNAME = Research ] ( ( EMPLOYEE ) JOIN ( DEPARTMENT ) ) ) "
query3="SELECT [ ESSN = 01 ] ( PROJECTION [ ESSN , PNAME ] ( ( WORKS_ON ) JOIN ( PROJECT ) ) )"
query4="PROJECTION [ BDATE ] ( ( EMPLOYEE ) JOIN ( DEPARTMENT ) ) "
query5="PROJECTION [ ESSN , PNAME ] ( ( WORKS_ON ) JOIN ( PROJECT ) )"
U=util()
line=U.read_sql(query3)
mytree=U.creat_tree(line)
treePlotter.createPlot(mytree)
# line=U.xuanze_chuanjie(line)
# line=U.xuanze_fenpei(line)
# line=U.touying_fenpei(line)
# mytree=U.creat_tree(line)
# treePlotter.createPlot(mytree)