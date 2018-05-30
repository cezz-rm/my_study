# flask基础操作

## 1.flask介绍

Flask是一个基于python实现的web开发的'微框架', 查看[官方文档](http://flask.pocoo.org/)

Flask和Django一样，也是一个基于MVC设计模式的Web框架

diango --> 完善完整高集成的框架

flask --> 不包含数据库抽象层微框架，database，templates需要自己去组装

Flask流行的主要原因：

- a) 有非常齐全的官方文档，上手非常方便
 
- b) 有非常好的拓展机制和第三方的拓展环境，工作中常见的软件都有对应的拓展，自己动手实现拓展也很容易
 
- c) 微型框架的形式给了开发者更大的选择空间
	
## 2.安装flask
创建虚拟环境
    
	virtualenv --no-site-packages flaskenv
启动虚拟环境，cd flaskenv \ cd Sript
    
	activate
安装
    
	pip install flask

## 3.创建flask项目
新建一个flask项目hello，hello.py文件如下
    
	from flask import Flask

	app = Flask(__name__)
	
	@app.route('/')
	def gello_world():
		return 'Hello World'
	
	if __name__ == '__main__':	
		app.run()

### 3.1 初始化

	from flask import Flask

	app = Flask(__name__)
Flask类构造函数唯一需要的参数就是应用程序的主模块或包。对于大多数应用程序，Python的__name__变量就是那个正确的、你需要传递的值。Flask使用这个参数来确定应用程序的根目录，这样以后可以相对这个路径来找到资源文件。

### 3.2 路由
	
	@app.route('/')
客户端例如web浏览器发送 请求 给web服务，进而将它们发送给Flask应用程序实例。应用程序实例需要知道对于各个URL请求需要运行哪些代码，所以它给Python函数建立了一个URLs映射。这些在URL和函数之间建立联系的操作被称之为 路由 。

在Flask应程序中定义路由的最便捷的方式是通过显示定义在应用程序实例之上的app.route装饰器，注册被装饰的函数来作为一个**路由**。

### 3.3 视图函数
在上一个示例给应用程序的根URL注册gello_world()函数作为事件的处理程序。如果这个应用程序被部署在服务器上并绑定了 www.example.com 域名，然后在你的浏览器地址栏中输入 http://www.example.com 将触发gello_world()来运行服务。客户端接收到的这个函数的返回值被称为 响应 。如果客户端是web浏览器，响应则是显示给用户的文档。

类似于gello_world()的函数被称作 **视图函数** 。

### 3.4 动态名称组件路由
你的Facebook个人信息页的URL是 http://www.facebook.com/ ，所以你的用户名是它的一部分。Flask在路由装饰器中使用特殊的语法支持这些类型的URLs。下面的示例定义了一个拥有动态名称组件的路由：
    
	@app.route('/hello/<name>')
	def gello_world(name):	
		return 'Hello World %s' % name
用尖括号括起来的部分是动态的部分，所以任何URLs匹配到静态部分都将映射到这个路由。当视图函数被调用，Flask发送动态组件作为一个参数。在前面的示例的视图函数中，这个参数是用于生成一个个性的问候作为响应。

在路由中动态组件默认为字符串，但是可以定义为其他类型。

django中

	\(\d+)\
	\<?P(\d+)>\

flask中

	<converter:name>
	string: 默认的字符串，可以省略
	int： 整型
	float：浮点型
	path：'/'也是当做字符串返回
	uuid:通用唯一识别码

### 3.5 服务启动
    
	if __name__ == '__main__':	
		app.run()
注意： __name__ == '__main__'在此处使用是用于确保web服务已经启动当脚本被立即执行。当脚本被另一个脚本导入，它被看做父脚本将启动不同的服务，所以app.run()调用会被跳过。

一旦服务启动，它将进入循环等待请求并为之服务。这个循环持续到应用程序停止，例如通过按下Ctrl-C。

有几个选项参数可以给app.run()配置web服务的操作模式。在开发期间，可以很方便的开启debug模式，将激活 debugger 和 reloader 。这样做是通过传递debug为True来实现的。

run()中参数有如下：
	
	debug 是否开启调试模式，开启后修改python的代码会自动重启

	port 启动指定服务器的端口号
	
	host主机，默认是127.0.0.1

## 4.修改启动方式，使用命令行参数启动服务
默认的启动方式：python xxx.py ---> 启动默认127.0.0.1:5000端口

还可导入sys模块的argv取得传入的参数

### 4.1 安装插件

	pip install flask-script
调整代码 manager = Manager(app=‘自定义的flask对象’)

启动的地方 manager.run()

### 4.2 启动命令
	
	python hellow.py runserver -h 地址 -p 端口 -d -r
其中：-h表示地址。-p表示端口。-d表示debug模式。-r表示自动重启

# flask基础操作进阶

## 1.什么是蓝图
在Flask项目中可以用Blueprint(蓝图)实现模块化的应用，使用蓝图可以让应用层次更清晰，开发者更容易去维护和开发项目。蓝图将作用于相同的URL前缀的请求地址，将具有相同前缀的请求都放在一个模块中，这样查找问题，一看路由就很快的可以找到对应的视图，并解决问题了。

## 2.使用蓝图

### 2.1 安装

	pip install flask-blueprint

### 2.2 实例化蓝图应用

	blue = Blueprint(‘first’，__name__)
注意：Blueprint中传入了两个参数，第一个是蓝图的名称，第二个是蓝图所在的包或模块，__name__代表当前模块名或者包名

### 2.3 注册

	app = Flask(__name__)

	app.register_blueprint(blue, url_prefix='/user')
注意：第一个参数即我们定义初始化定义的蓝图对象，第二个参数url_prefix表示该蓝图下，所有的url请求必须以/user开始。这样对一个模块的url可以很好的进行统一管理

## 3.使用蓝图
修改视图上的装饰器，修改为@blue.router(‘/’)
	
	@blue.route('/', methods=['GET', 'POST'])
	def hello():
	    # 视图函数
	    return 'Hello World'
注意：该方法对应的url为127.0.0.1:5000/user/