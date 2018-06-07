# flask插件

### 1. 开发，页面调试工具debugtoolbar

#### 1.1 安装

	pip install flask-debugtoolbar

#### 1.2 配置

	from flask import Flask

	from flask_debugtoolbar import DebugToolbarExtension
	
	app = Flask(__name__)
	
	app.debug = True
	
	app.config['SECRET_KEY'] = '<replace with a secret key>'
	
	toolbar = DebugToolbarExtension(app)

# flask项目部署

1. 更新ubuntu的源

	sudo apt-get update

2. 安装mysql

	sudo apt install mysql-server mysql-client

3. 修改mysql配置

	cd /etc/mysql/mysql.conf.d
	修改mysqld.conf 讲bind_address注释

4. 修改配置

	use mysql；

	GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;

	flush privileges; 

5. 重启mysql
	
	service mysql restart


6. 安装Nginx：

	sudo apt-get install nginx

7. 安装pip3

	apt install python3-pip


8. 安装uWSGI以及uWSGI对于Python的支持：

	pip3 install uwsgi

9. 修改总的nginx的配置的文件

	vim /etc/nginx/nginx.conf

10. 配置nginx的文件

	server {
	listen 80;
	server_name 47.92.73.20 localhost;
	
	access_log /home/app/logs/access.log;
	error_log /home/app/logs/error.log;
	
	location / {
	include uwsgi_params;
	uwsgi_pass 127.0.0.1:8890;
	
	
	uwsgi_param UWSGI_CHDIR /home/app/src/s_aj;
	
	uwsgi_param UWSGI_SCRIPT manage:app; # 启动flask的文件:Flask的实例
	
	}

	}



11. 配置uwsgi的文件

	[uwsgi]
	
	socket=127.0.0.1:8890
	
	pythonpath=/home/app/src/s_aj; #项目所在目录
	
	callable=app; # 回调的flask实例
	
	logto = /home/app/logs/uwsgi.log # 存uwsgi日志的文件地址
