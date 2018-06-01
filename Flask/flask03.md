学习笔记大纲

	1. 挖坑
	block  endblock
	
	2. 加载css
	
	django：
	第一种方式：
	{% load static %}
	<link rel="stylesheet" href="{% static 'css/index.css' %}">
	
	第二种方式：
	<link rel="stylesheet" href="/static/css/index.css">
	
	
	flask：
	第一种方式：
	<link rel="stylesheet" href="/static/css/index.css">
	
	第二种方式：
	<link rel="stylesheet" href="{{ url_for('static', filename='css/index.css') }}">
	
	3. 过滤器
	
	safe：渲染标签
	striptags：渲染之前去掉标签
	
	trim：去掉空格
	length：计算长度
	
	第一个字母{{ i|first }}
	最后一个字母{{ i|last }}
	小写{{ i|lower }}
	大写{{ i|upper }},
	首字母大写{{ i|capitalize }}
	
	4. 数据库
	
	pip install flask-sqlalchemy
	pip install pymysql
	
	primary_key：指定主键
	autoincrement：自增
	unique：唯一
	default：默认值
	Integer：整形
	String：字符串
	
	__tablename__：指定数据库名称
	
	SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:123456@localhost:3306/flask3'
	
	5. 事务
	
	原子性，一致性，隔离性，持久性


# flask模板

## jinjia2

Flask中使用的是jinjia2模板引擎

jinjia2是由Flask作者开发， 模仿Django的模板引擎

优点：

	速度快，被广泛使用
	
	HTML设计和后端python分离

	非常灵活， 快速和安全

	提供了控制，继承等高级功能

## 模板语法

### 模板语法主要分为两种：变量和标签

模板中的变量: {{ var }}

	视图传递给模板的数据

	前面定义出来的数据

	变量不存在，默认忽略

模板中的标签: {% tag %}

	控制逻辑

	使用外部表达式

	创建变量

	宏定义

### 结构标签

block

	{% block XXX %}

	{% endblock %}

	块操作
		父模板挖坑，子模板填坑

extends
	
	{% extends 'xxx.html' %}

	继承以后保留块中的内容
	{% super() %}

挖坑继承体现的化整为零的操作


marco

	{% marco hello(name) %}

		{{ name }} 

	{% endmarco %}

	宏定义，可以在模板中定义函数，在其他地方调用

宏定义可导入

	{% from 'xxx' import xxx %}


例子1：

在index.html中定义marco标签，定义一个方法，然后去调用方法，结果是展示商品的id和商品名称


	{% marco show_goods(id, name) %}
		商品id: {{ id }}
		商品名称: {{ name }}
	{% endmacro %}

	{{ show_goods('1', '娃哈哈') }}
	
	{{ show_goods('2', '雪碧') }}

例子2：

定义一个function.html中定义一个方法:

	{% marco say() %}

		<h3>今天天气气温回升</h3>
		<h3>适合去游泳</h3>
		<h3>适合去郊游</h3>

	{% endmacro %}

例子3:

定义一个function.html中定义一个方法

	{% marco create_user(name) %}
		创建了一个用户:{{name}}
	{% endmacro %}

在index.html中引入function.html中定义的方法
		
	{% from 'functions.html' import create_user %}

	{{ create_user('小花') }}


### 循环

	{% for item in cols %}

		aa

	{% else %}

		bb

	{% endfor %}

也可以获取循环信息loop
	
	loop.first

	loop.last

	loop.index

	loop.revindex

### 过滤器

语法：

	{{ 变量|过滤器|过滤器... }}

capitalize 单词首字母大写

lower 单词变为小写

upper 单词变为大写

title

trim 去掉字符串的前后的空格

reverse 单词反转

format

striptags 渲染之前， 将值中标签去掉

safe 将样式渲染到页面中

default

last 最后一个字母

first

length

sum

sort

## 定义模板

### 定义基础模板base.html

	<!DOCTYPE html>
	<html lang="en">
	<head>
	    <meta charset="UTF-8">
	    <title>
	        {% block title %}
	        {% endblock %}
	    </title>
	    <script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
	
	    {% block extCSS %}
	    {% endblock %}
	</head>
	<body>

	{% block header %}
	{% endblock %}
	
	{% block content%}
	{% endblock %}
	
	{% block footer%}
	{% endblock %}
	
	{% block extJS %}
	{% endblock %}

	</body>
	</html>


### 定义基础模板base_main.html

	{% extends 'base.html' %}
	
	{% block extCSS %}
	    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
	{% endblock %}


# flask模型

### 1. Flask模型

Flask默认并没有提供任何数据库操作的API

我们可以选择任何适合自己项目的数据库来使用

Flask中可以自己的选择数据，用原生语句实现功能，也可以选择ORM（SQLAlchemy，MongoEngine）

SQLAlchemy是一个很强大的关系型数据库框架，支持多种数据库后台。SQLAlchemy提供了高层ORM，也提供了使用数据库原生SQL的低层功能。

ORM：

	将对对象的操作转换为原生SQL
	优点
		易用性，可以有效减少重复SQL
		性能损耗少
		设计灵活，可以轻松实现复杂查询
		移植性好

针对于Flask的支持，[官网地址](http://flask-sqlalchemy.pocoo.org/2.3/)

	pip install flask-sqlalchemy
	
安装驱动

	pip install pymysql

### 2. 定义模型

使用SQLALchemy的对象去创建字段

其中__tablename__指定创建的数据库的名称

	创建models.py文件，其中定义模型

	from flask_sqlalchemy import SQLAlchemy
	
	db = SQLAlchemy()
	
	
	class Student(db.Model):
	
	    s_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	    s_name = db.Column(db.String(16), unique=True)
	    s_age = db.Column(db.Integer, default=1)
	
	    __tablename__ = "student"

其中：

Integer表示创建的s_id字段的类型为整形，

primary_key表示是否为主键

String表示该字段为字符串

unique表示该字段唯一

default表示默认值

autoincrement表示是否自增


### 3. 创建数据表

在视图函数中我们引入models.py中定义的db

	from App.models import db
	
	@blue.route("/createdb/")
	def create_db():
	    db.create_all()
	    return "创建成功"
	
	@blue.route('/dropdb/')
	def drop_db():
	    db.drop_all()
	    return '删除成功'


其中： db.create_all()表示创建定义模型中对应到数据库中的表

db.drop_all()表示删除数据库中的所有的表



### 4. 初始化SQLALchemy

在定义的__init__.py文件中使用SQLALchemy去整合一个或多个Flask的应用

有两种方式：

	第一种：

	from flask_sqlalchemy import SQLALchemy
	
	app = Flask(__name__)
	    db = SQLAlchemy(app)

	第二种：

	db = SQLAlchemy()
	
    def create_app():
        app = Flask(__name__)
        db.init_app(app)
        return app


### 5. 配置数据库的访问地址

[官网配置参数](http://www.pythondoc.com/flask-sqlalchemy/config.html)

数据库连接的格式：

	dialect+driver://username:password@host:port/database

	dialect数据库实现
	
	driver数据库的驱动

例子：
访问mysql数据库，驱动为pymysql，用户为root，密码为123456，数据库的地址为本地，端口为3306，数据库名称HelloFlask

设置如下： "mysql+pymysql://root:123456@localhost:3306/HelloFlask"

在初始化__init__.py文件中如下配置：

	app.config['SQLALCHEMY_TRAKE_MODIFICATIONS'] = False

    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost:3306/HelloFlask"

### 6. 对学生数据进行CRUD操作

语法：

	类名.query.xxx

获取查询集：

	all()
	
	filter(类名.属性名==xxx)

	filter_by(属性名=xxx)

数据操作：

	在事务中处理，数据插入

	db.session.add(object)

	db.session.add_all(list[object])
	
	db.session.delete(object)

	db.session.commit()
	
	修改和删除基于查询



#### 6.1 想学生表中添加数据

	@blue.route('/createstu/')
	def create_stu():
	
	    s = Student()
	    s.s_name = '小花%d' % random.randrange(100)
	    s.s_age = '%d' % random.randrange(30)
	
	    db.session.add(s)
	    db.session.commit()
	
	    return '添加成功'

提交事务，使用commit提交我们的添加数据的操作

#### 6.2 获取所有学生信息

将学生的全部信息获取到，并且返回给页面，在页面中使用for循环去解析即可

	@blue.route("/getstudents/")
	def get_students():
	    students = Student.query.all()
	    return render_template("StudentList.html", students=students)

#### 6.3 获取s_id=1的学生的信息

写法1：

	students = Student.query.filter(Student.s_id==1)

写法2：

	students = Student.query.filter_by(s_id=2)

注意：filter中可以接多个过滤条件

写法3：
	
	sql = 'select * from student where s_id=1'
    students = db.session.execute(sql)

#### 6.4 修改学生的信息

写法1：

    students = Student.query.filter_by(s_id=3).first()
    students.s_name = '哈哈'
    db.session.commit()

写法2：

	Student.query.filter_by(s_id=3).update({'s_name':'娃哈哈'})
 
    db.session.commit()

#### 6.5 删除一个学生的信息

写法1：

    students = Student.query.filter_by(s_id=2).first()
    db.session.delete(students)
    db.session.commit()

写法2：

    students = Student.query.filter_by(s_id=1).all()
    db.session.delete(students[0])
    db.session.commit()

注意：filter_by后的结果是一个list的结果集

<b>重点注意：在增删改中如果不commit的话，数据库中的数据并不会更新，只会修改本地缓存中的数据，所以一定需要db.session.commit()</b>

	