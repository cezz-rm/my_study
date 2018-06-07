### 1.添加多条学生信息

s_list = [学生对象1， 学生对象2，]

db.session.add_all(s_list)

要同时向数据库中添加多条数据，可将数据放在列表中，再使用add_all添加即可，具体如下

	stus_list = []
    username1 = request.form.get('username1')
    age1 = request.form.get('age1')

    username2 = request.form.get('username2')
    age2 = request.form.get('age2')

    stu1 = Student(username1, age1)
    stu2 = Student(username2, age2)

    stus_list.append(stu1)
    stus_list.append(stu2)

    db.session.add_all(stus_list)
    db.session.commit()
		

### 2.运算符

\_\_lt__ 小于

\_\_le__ 小于等于

\_\_gt__ 大于

\_\_ge__ 大于等于

in_ 在范围内

order_by 排序

limit 截取几个信息

offset 跳过几个信息

get 获取主键对应的信息

and_ 并且条件

or_ 或者条件

not_ 非

具体例子如下：

filter(模型名.字段 运算符 值)

	# 年龄小于16岁的学生的信息
    stus = Student.query.filter(Student.s_age < 16)

filter(模型名.字段.运算符('xxx'))

	# 小于__lt__ /小于等于__le__ /大于__gt__ /大于等于__ge__
    stus = Student.query.filter(Student.s_age.__lt__(16))
    stus = Student.query.filter(Student.s_age.__le__(16))

    # 年龄在12, 11, 99的
    stus = Student.query.filter(Student.s_age.in_([11, 12, 99]))

    # 获取所有学生信息
    sql = 'select * from student;'
    stus = db.session.execute(sql)

    # 按照id降序排列
    stus = Student.query.order_by('-s_id')

    # 按照id降序获取三个
    stus = Student.query.order_by('-s_id').limit(3)

    # 获取年龄最大的一个
    stus = Student.query.order_by('-s_age').first()

    # offset跳过几个数据， limit查询几个数据
    stus = Student.query.order_by('-s_age').offset(2).limit(2)

    # 获取id等于3的学生
    stus = Student.query.filter(Student.s_id == 3)
    stus = Student.query.get(3)

    # 查询多个条件
    stus = Student.query.filter(Student.s_age == 11, Student.s_name == '王大锤')

    # and_  并且条件
    stus = Student.query.filter(and_(Student.s_age == 11, Student.s_name == '王大锤'))

    # or_  或者条件
    stus = Student.query.filter(or_(Student.s_age == 11, Student.s_name == '小乔'))

    # not_  非
    stus = Student.query.filter(not_(Student.s_age == 11))


### 3.分页

paginate对象

pages 总页数

total 总条数

has_prev 是否有上页

has_next 是否有下页

prev_num

next_num

iter_pages() 当前一共多少页[1,2,3]

### 4.one_to_many


在one的model中定义relationship字段 

	students = db.relationship('Student', backref='stu', lazy=True)

在many的model中定义关联外键的字段s_g

	s_g = db.Column(db.Integer, db.ForeignKey('grade.g_id'), nullable=True)



1）通过one找many，one的对象.students，结果为many的结果

2）通过many找one，many的对象.stu，结果为one的对象

模型如下：
	
	class Student(db.Model):
	
	    s_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	    s_name = db.Column(db.String(20), unique=True)
	    s_age = db.Column(db.Integer, default=18)
	    s_g = db.Column(db.Integer, db.ForeignKey('grade.g_id'), nullable=True)
	
	    __tablename__ = 'student'
	
	    def __init__(self, name, age):
	
	        self.s_name = name
	        self.s_age = age
	
	
	class Grade(db.Model):
	
	    g_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	    g_name = db.Column(db.String(10), unique=True)
	    g_desc = db.Column(db.String(100), nullable=True)
	    g_time = db.Column(db.Date, default=datetime.datetime.now())
	    students = db.relationship('Student', backref='stu', lazy=True)
	
	    __tablename__ = 'grade'
	
	    def __init__(self, name, desc):
	        self.g_name = name
	        self.g_desc = desc
		
通过one的模型查找many的模型

	@grade.route('/selectstubygrade/<int:id>/')
	def select_stu_by_grade(id):
	
	    grade = Grade.query.get(id)
	    stus = grade.students
	    return render_template('grade_student.html',
	                           grade=grade,
	                           stus=stus)

通过many的模型查找one的模型

	@stu.route('/selectgradebystu/<int:id>/')
	def select_grade_by_stu(id):
	    stu = Student.query.get(id)
	    grade = stu.stu
	    return render_template('student_grade.html',
	                           grade=grade,
	                           stu=stu)