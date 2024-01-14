# coding=utf-8
from util import util
query1="SELECT [ ENAME = ' Jack ' & DNAME = ' Reserach '] ( ( EMPLOYEE ) JOIN ( DEPARTMENT ) )"
query2="PROJECTION [ BDATE ] ( SELECT [ ENAME = John & DNAME = Research ] ( ( EMPLOYEE ) JOIN ( DEPARTMENT ) ) ) "
query3="SELECT [ ESSN = 01 ] ( PROJECTION [ ESSN , PNAME ] ( ( WORKS_ON ) JOIN ( PROJECT ) ) )"

im = util()
im.merge(query1)
# im.merge(query2)
# im.merge(query3)