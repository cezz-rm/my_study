# Django项目部署
将Django中的DEBUG设置为False的时候， 'django.contrib.staticfiles'会关闭，Django就不会自动搜索并加载静态文件，可以使用Django来处理静态文件，也可以使用nginx处理静态文件。
## 部署一:
(本文使用的linux系统为ubuntu)

### 1. 安装包
sudo apt update

apt install mysql-server mysql-client

### 2. 设置远程访问mysql

	a) 查找 mysql.conf 配置文件 
		find / -name mysql.cnf
	b）注释mysql.cof文件的bind_address，允许远程连接访问
		/etc/mysql/mysql.conf.d

	c）切换mysql数据库
		use mysql;
	d) 重启
		service mysql start/restart/stop	
		
		给root用户远程访问权限，其中'root@123'为访问密码
		GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root@123' WITH GRANT OPTION;

		刷新用户权限
		flush privileges; 

### 3. 修改django的配置文件

	a）修改settings.py文件中的DEBUG=FALSE，ALLOWED_HOST=['*']
	b）修改urls.py

		b1）from django.views.static import serve
		url中加入以下配置
		url(r'^static/(?P<path>.*)$', serve, {"document_root": settings.STATIC_ROOT}),
		url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),

		b2）setting中
		STATIC_ROOT = os.path.join(BASE_DIR, 'static')

		b3）url中修改首页访问的地址
		url(r'^$', views.home)


### 4. 修改首页的启动地址

	修改工程目录中的url ，并修改url(r'^$', views.home)

### 5. 安装pip3

	apt install python3-pip

### 6. 安装必备库

	pip3 install django==1.11
	pip3 install pymysql
	pip3 install Pillow

### 7. 查看进程

 	netstat -lntp

### 8. 启动项目

	python3 manage.py runserver 0.0.0.0:8080

## 部署二
使用nginx+uwsgi配置django项目

### 1. 安装nginx
sudo apt-get install nginx
	
### 2. 查看nginx的状态

systemctl status nginx 查看nginx的状态

systemctl start/stop/enable/disable nginx 启动/关闭/设置开机启动/禁止开机启动

service nginx status/stop/restart/start

### 3. 安装uwsgi
pip install uwsgi

### 4. nginx的配置文件中加载自定义的nginx的配置文件

	vim /etc/nginx/nginx.conf
	在server中加入以下配置：
	include /home/app/conf/*.conf;


### 5. 配置自定义的nginx配置文件

	server {
	    listen       80;
	    server_name 47.92.164.198 localhost;

	    access_log /home/app/log/access.log;
	    error_log /home/app/log/error.log;

	    location / {
	        include uwsgi_params;
	        uwsgi_pass 127.0.0.1:8890;
	    }
	    location /static/ {
	        alias /home/app/src/static/;
	        expires 30d;
	    }

	}

爱鲜蜂项目上线配置文件axf.conf如下

	server {
            listen       80;
            server_name 119.23.230.164 localhost;

            access_log /home/app/log/access.log;
            error_log /home/app/log/error.log;

            location / {
                include uwsgi_params;
                uwsgi_pass 127.0.0.1:8890;
            }
            location /static/ {
                alias /home/app/src/AXF/static/;
                expires 30d;
            }
}

### 6. 配置uwsgi，名称为uwsgi.ini
	
	[uwsgi]
	# variables
	projectname = AXF
	newprojectname = AXF
	base = /home/app

	# config
	#plugins = python
	master = true
	#protocol = uwsgi
	processes = 4
	#env = DJANGO_SETTINGS_MODULE=%(projectname).settings
	pythonpath = %(base)/src/%(projectname)
	module = %(newprojectname).wsgi
	socket = 127.0.0.1:8890
	logto = %(base)/log/uwsgi.log

爱鲜蜂项目uwsgi.ini配置文件如下

	
	[uwsgi]

	master = true
	
	processes = 4
	
	pythonpath = /home/app/src/AXF
	
	module = AXF.wsgi
	
	socket = 127.0.0.1:8890
	
	logto = /home/app/log/uwsgi.log


### 启动方式： uwsgi --ini uwsgi.ini