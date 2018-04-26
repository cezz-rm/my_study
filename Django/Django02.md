# 项目连接MySQL数据库
### 1.修改配置文件
需修改settings.py中配置数据库的连接信息DATABASE如下所示

    DATABASES = {
    	'default': {
        	'ENGINE': 'django.db.backends.mysql',
        	'USER': 'root',
        	'PASSWORD': '482185',
        	'PORT': '3306',
       		'HOST': 'localhost',
        	'NAME': 'day02_1',
    	}
	}
### 2.在mysql中创建好定义的数据库
##### ①.进入mysql
**mysql -u root -p**
##### ②.创建数据库
**create database XXX charset=utf-8;**

### 3.配置数据库链接
##### ①.安装pymysql
**pip install pymysql**
##### ②.配置__init__.py文件，完成数据库的驱动加载
**import pymysql**<br>
**pymysql.install\_as\_MySQLdb()**

### 4.定义模型
在文件models.py下定义一个模型类<br>
一个模型类在数据库中对应一张表,在模型类中定义的属性，对应模型对照表中的一个字段

    from django.db import models

	# Create your models here.


	class Student(models.Model):
	    stu_name = models.CharField(max_length=6)
	    stu_sex = models.BooleanField()
	    stu_birth = models.DateField()
	    stu_delete = models.BooleanField(default=0)
	    stu_create_time = models.DateField(auto_now_add=True)
	    stu_operate_time = models.DateField(auto_now=True)
	    stu_tel = models.CharField(max_length=11)
	
	    class Meta:
	        db_table = 'stu02_1'

### 5.迁移数据库
- 生成迁移文件 python manage.py makemigrations
- 执行迁移生成数据库 python manage.py migrate
>> 注意：如果提示no changes detected, 可以将数据库中的表django_migrations中为appname的字段

### 6.ORM
ORM(Objects Relational Mapping)对象关系映射,是一种程序技术，用于实现面向对象编程语言里不同类型系统的数据之间的转换。可以简单理解为翻译机。


# admin管理后台
### 1.准备工作
在创建的app-stu下的model.py中定义Student的模型

    from django.db import models
    
    # Create your models here.
    
    
    class Student(models.Model):
    	name = models.CharField(max_length=10)
    	sex = models.BooleanField()
    
    	class Meta:
   			db_table = 'student'

admin管理后台的url<br>
在项目的urls.py文件下可看到路由配置中有一个admin的url地址<br>
**url(r'^admin/', admin.site.urls)**
### 2.创建admin后台的用户密码
python manage.py createsuperuser
### 3.在登录后的管理后台中对自定义的模型进行CRUD操作
ORM 对象关系映射，翻译机

# 模型字段
## 字段类型
#### AutoField
一个根据实际ID自动增长的IntegerField，通常不指定(将一个主键字段自动添加到模型中)。
#### CharField(max_length=字符长度)
字符串，默认的表单样式是TextInput
#### TextField
大文本字段，一般超过4000使用，默认的表单控件是Textarea
#### IntegerField
整数
#### DecimalField(max_digits=None, decimal_places=None)
使用python的Decimal实例表示十进制的浮点数<br>
max_digits 位数总数<br>
decimal_places 小数点后的数字位数
#### FloatField
用python的float实例来表示的浮点数
#### BooleanField
true/false字段, 此字段的默认表单控制是CheckboxInput
#### NullBooleanField
支持null, true, false三种值
#### DateField([auto_now=False, auto_now_add=False])
使用python的datetime.date实例表示的日期<br>
auto_now:每次修改的时候赋值,默认值为False<br>
auto_now_add:第一次创建的时候赋值，默认值为False
#### TimeField
使用Python的datetime.date表示的时间，参数同DateField
#### DateTimeField
使用python的datetime.datetime实例表示的日期和时间,参数同Datefield
#### FileField
一个上传文件的字段
#### ImageField
继承了FileField的所有属性和方法,但对上传的对象进行校验，确保它是个有效的image<br>
upload_to=""  指定上传图片的路径


## 模型参数
- default: 默认值
- null: 设置是否为空， 针对数据库中该字段是否可以为空， 默认为False
- blank： 设置是否为空， 针对表单提交该字段是否可以为空， 默认为False
- db_column: 字段的名称。未指定的话默认为属性的名称
- db_index:若值为True，则在表中会为此字段创建索引
- primary_key: 若为True，则该字段会成为模型的主键字段
- unique: 如果为True，这个字段在表中必须有唯一值

# 模型练习
#### 1.数据库准备

在model中定义数据库,其中的性别，男的存1，女的存0。

    class Student(models.Model):
        stuname = models.CharField(max_length=20)
        studex = models.BooleanField()
        stubirth = models.DateField()
        stutel = models.CharField(max_length=255)

        class Meta:
            db_table = 'student'
    
#### 2.数据库迁移

    python manage.py makemigrations
	python manage.py migrate

#### 3. 数据插入

##### 3.1 使用表单form提交post请求数据

	<form action="/app/addStu/" method="post">
	    stuname: <input type="text" name="name">
	    stusex: <input type="text" name="sex">
	    stubirth: <input type="date" name="birth">
	    stutel: <input type="text" name="tel">
	    <input type="submit" value="提交">
	</form>

##### 3.2 获取post请求，获取请求数据，并且创建数据

	方法1：
    stu = Student()
    stu.stuname = stuname
    stu.stusex = sex
    stu.stubirth = birth
    stu.stutel = tel
    stu.save()

    方法2：
    Student.objects.create(stuname=stuname, stusex=sex, stubirth=birth, stutel=tel)


#### 4. 查询所有的学生信息
使用all()方法获取所有的数据

	Student.objects.all()

#### 5. 查询所有女学生的姓名和出生日期

	Student.objects.filter(stusex=0)
	或者
	Student.objects.exclude(stusex=1)

其中：
filter():返回符合条件的数据<br>
exclude():过滤掉符合条件的数据

#### 6.查询所有的学生，按照id从大到小排序

	Student.objects.all().order_by('-id')

其中：
order_by('id'):表示按照id升序的排列<br>
order_by('-id'):表示按照id降序的排列

#### 7. 查询单个数据，就不做演示了，可以使用以下的方法去获取

get()：返回一个满足条件的对象。如果没有返回符合条件的对象，会应该模型类DoesNotExist异常，如果找到多个，会引发模型类MultiObjectsReturned异常

first()：返回查询集中的第一个对象

last()：返回查询集中的最后一个对象

count()：返回当前查询集中的对象个数

exists()：判断查询集中是否有数据，如果有数据返回True，没有返回False

#### 7.查询所有80后学生的姓名、性别和出生日期(筛选)

	Student.objects.filter(stubirth__gte='1980-01-01', stubirth__lte='1990-01-01')

#### 8.查询名字中有王字的学生的姓名(模糊)

	Student.objects.filter(stuname__contains='王')

#### 9.查询姓王的学生姓名和性别(模糊)

	Student.objects.filter(stuname__startswith='王')