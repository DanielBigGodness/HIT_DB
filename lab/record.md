管理客户信息，包括客户编号、姓名、性别、出生日期、电话、身高、体重、主管教练（可以没有）

 

 

CREATE TABLE customers (
​    Num CHAR(10) PRIMARY KEY,
​    Name CHAR(10) NOT NULL,
​    Sex CHAR(1) NOT NULL,
​    Birthday DATE NOT NULL,
​    Tel CHAR(11) NOT NULL,
​    Height INT NOT NULL,
​    Weight INT NOT NULL,
​    Coach_num CHAR(10),
​    CONSTRAINT chk_sex CHECK (Sex IN ('M', 'F'))
);

 

INSERT INTO customers
VALUES (
'2021112522',
'guojiahe',
'M',
'2004-02-28',
'13030700999',
'195',
'105',
NULL
);

 show_table --table customers --length 10
delete --table customers --limit Sex='F'
 insert --table customers --values 201121,shushu,M,2020-10-10,11111111100,130,130,002




管理教练信息，包括教练编号、姓名、性别，出生日期、电话、擅⻓的健身项目（不止一种）

CREATE TABLE coaches (
​    Num CHAR(10) PRIMARY KEY,
​    Name CHAR(10) NOT NULL,
​    Sex CHAR(1) NOT NULL,
​    Birthday DATE NOT NULL,
​    Tel CHAR(11) NOT NULL,
​    GoodAt SET ('跑步','游泳','杠铃'),
​    CONSTRAINT chk_sex CHECK (Sex IN ('M', 'F'))
);

 INSERT INTO coaches
VALUES (
'001',
'jiaolian1',
'M',
'2004-01-28',
'13030600999',
('跑步,游泳')
);

客户: 编号,名字,性别,生日,电话,身高,体重,教练编号
​         Num,Name,Sex,Birthday,Tel,Height,Weight,Coach_num
教练: 编号,名字,性别,生日,电话,擅长项目(跑步游泳杠铃)
​         Num,Name,Sex,Birthday,Tel,GoodAt

2021,shushu,M,2020-10-10,11111111100,游泳



001,kehu1,M,2020-10-10,11111111100,130,130,002



001@kehu1@M@2020-10-10@11111111100@130@130@002

003@jiaolian3@F@2021-10-10@11111111100@游泳,杠铃


分组查询

select Name from customers where Sex='M'  group by Num having COUNT(*)=1;



添加外键

ALTER TABLE table_name ADD CONSTRAINT <外键名> FOREIGN KEY <字段> REFERENCES <主表名> <主表字段>；

ALTER TABLE customers ADD CONSTRAINT Coach_num_CONSTRAINT FOREIGN KEY (Coach_num)  REFERENCES coaches(Num);





管理健身项目信息，包括健身项目名称、项目安排（时间、场馆、教练）

 

 

管理健身记录，包括客户每次训练的开始时间、结束时间、训练场馆、教练信息、训练项目

 













remake

CREATE TABLE students (
​    stu_id CHAR(10) PRIMARY KEY,
​    name CHAR(10) NOT NULL,
​    sex CHAR(1) NOT NULL, 
​    birthday DATE NOT NULL,
​    CONSTRAINT chk_sex CHECK (sex IN ('M', 'F'))
);

CREATE TABLE classes (
​    class_id CHAR(10) PRIMARY KEY,
​    name CHAR(10) NOT NULL,
);

