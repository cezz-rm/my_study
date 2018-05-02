# 视图与网址进阶
## 视图一

### 一、url配置
#### 1.配置流程
配置settings.py文件下的ROOT_URLCONF属性值
    
	ROOT_URLCONF = 'day05_1.urls'
#### 2.urlpatterns
在项目下新建urls.py文件，然后创建一个url的实例对象，正则匹配
    
	urlpatterns = [
    url(r'index/', views.index),
	]
#### 3.将项目下的url配置导入工程目录
    
	from django.conf.urls import url, include
	urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^stu/', include('stu.urls', namespace='s')),
	]
>正则匹配注意事项:
>
- 正则匹配时从上到下进行遍历，匹配到就不会继续向后查找了
- 匹配的正则前方不需要加反斜杠
- 正则钱需要加（r）表示字符串不转义

### 二、获取url路径的参数
#### 1.url传递一个参数
要从url中获取一个参数，括号里写正则表达式，如下
    
	url(r‘^grade/(\d+)/’, views.addStuInfo, name='addinfo')
要明确该值是传个哪个变量的:
    
	url(r'addinfo/(?P<stu_id>\d+)/', views.addStuInfo, name='addinfo')
>注意：url中添加了()传参，则在调用函数中必须接收 def addStuInfo(request, stu_id)

#### 2.url传递多个参数 
要获取url中的多个参数，可以添加多个括号，若不指定变量名，则按默认顺序进行匹配
	
	url(r'selstu/(\d+)/(\d+)/(\d+)/', views.selStu),
	或
    url(r'adtstu/(?P<year>\d+)/(?P<month>\d+)/(?P<days>\d+)/', views.actStu),
实现方法
    
	def selStu(request, m, n, p):
    	return HttpResponse('获取url传递多个参数')
	或
	def actStu(request, year, month, days):
    	return HttpResponse('获取传递的指定参数')

### 三、反向解析
使用反向解析优点:

如果在视图中，模板中使用硬编码连接，在url配置发生改变时，需要变更的代码会非常多，这样导致我们的代码结构不是很容易维护，使用反向解析可以提高我们代码的扩展性和可维护性
#### 1.在模板中进行反向解析
关键字参数:{% url 'namespace:name' key1=value1 key2=value2 %}

    url(r'^s/', include('stu.urls', namespace='s'))
	
	url(r'allstu/(\d+)/', views.allStu, name='alls')

	<a href="{% url 's:alls' g.id %}"></a>
#### 2.在views中使用反向解析
    
	from django.core.urlresolvers import reverse
	
	HttpResponseRedirect(
		reverse(namespace:name, kwargs = {key1 : value1, key2 : value2})
	)

例如
    
	def allStu(request, g_id):
	    return HttpResponseRedirect(
	        reverse('s:reStu', kwargs={'g_id': g_id})
	    )


	def redirectStu(request, g_id):
	    stus = Student.objects.filter(g_id=g_id)
	    return render(request, 'students.html', {'stus': stus })
### 四、视图
#### 1.错误视图
通常在项目下的views.py中定义

- 404视图（页面没有被找到 page not found） 
- 400视图（客户端操作错误 bad request） 
- 403视图（权限错误 403 forbidden ） 
- 500视图（服务器内部错误 server error）

在工程下的urls.py文件下添加如下代码:
    
	from grade.views import page_not_found, server_error, permission_denied

	handler404 = page_not_found
	handler500 = server_error
	handler403 = permission_denied
然后在项目下的views.py文件下定义方法：
    
	def page_not_found(request):
    	return render(request, '404.html')

	def server_error(request):
    	return render(request, '500.html')

	def permission_denied(request):
		return render(request, '403.html')
#### 2.自定义错误视图
在settings.py文件中修改debug模式
    
	DEBUG = True

	ALLOWED_HOSTS = []
改为
    
	DEBUG = False

	ALLOWED_HOSTS = ["*"]
将不显示错误详情，且所有ip地址都可连接
### 五、请求与响应
#### 1.HttpRequest定义
服务器在接收到http请求后，会根据报文创建HttpRequest对象
视图中第一个参数就是HttpRequest对象
Django框架会进行自己的包装，之后传递给视图。

属性：

- path       &nbsp;&nbsp; 请求的完整路径
- method     &nbsp;&nbsp; 请求的方法，通常get，post
- Encoding   &nbsp;&nbsp; 编码方式，常用utf-8
- Get        &nbsp;&nbsp; 类似字典的参数，包含了get的所有参数
- post	     &nbsp;&nbsp; 类似字典的参数，包含了post的所有参数
- Files      &nbsp;&nbsp; 类似字典的参数，包含了上传的文件
- Cookies    &nbsp;&nbsp; 字典，包含了所有的COOKIES
- Session    &nbsp;&nbsp; 类似字典，表示会话
- 方法： is_ajax()  &nbsp;&nbsp; 判断是否是ajax()，通常在移动端和js中

#### 2.响应QueryDict类型

	1）类似字典的结构数据，与字典的区别，可以存在相同的键

	2）GET和POST都是QueryDict对象

	3）QueryDict中数据获取方式
        dict[‘name’] 或者dict.get(‘name’)
        获取指定key对应的所有值
        dict.getlist(‘name’)

#### 3.响应

	1）可以直接返回一个HttpResponse对象：
    	服务器返回给客户端的数据，HttpResponse由程序员自己创建
    	不使用模板，直接HttpResponse()

	2）可以返回模板
	调用模板，进行渲染，直接使用render一步到位
	返回表达式：
	    render(request, template_name, context)
	        request  请求体对象
	        template_name  模板路径
	        context  字典参数，用来填坑

	3）属性
	    Content   返回的内容
	    Charset   编码格式
	    status_code  响应状态码（200,4xx,5xx）
	        4xx 客户端的错误
	        5xx 服务端的错误
    	content_type   MIME类型，定义传输类型的，比如有xml，html，png等等，比如content_type=’image/jpg’
	4）方法
	    init    初始化内容
	    write(xxx) 直接写到文本
	    flush 冲刷缓冲区
	    set_cookie(key, value=’’, max_age=None, exprise=None)
	    delete_cookie(key)   删除cookie，上面是设置
	4）重定向
	    HttpResponseRedirect响应重定向：可以实现服务器内部的跳转
	    Return HttpResponseRedirect(‘/xxx/xxx’)
	    使用的时候推荐使用反向解析
	    JsonResponse
	    使用json数据的请求，通常用在异步请求上jsonResponse(dict)
	    content_type是application/json
## 视图二
### 一、cookie
#### 1.描述
浏览器端的回话技术,cookie本身由浏览器生成，通过Response将cookie写在浏览器上，下一次访问，浏览器会根据不同的规则携带cookie过来

#### 2.设置cookie
    
	response.set_cookie(key, value, max_age=None, exprise=None)
    request.GET.get(key)
>注意：cookie不能跨浏览器

参数定义：
    
	max_age :  整数，指定cookie过期时间，以秒为单位
    exprise： 整数，指定过期时间，还支持是一个datetime或者timedelta，可以指定一个具体日期时间
    max_age和exprise两个选一个指定
    过期时间的几个关键时间
    max_age设置为0浏览器关闭失效
    设置位None永不过期
    exprise=timedelta(days=10) 10天后过期
### 二、session
#### 1.描述
服务端会话技术，依赖于cookie

#### 2.开启session设置
django中启用SESSION 在settings中修改如下地方
    
	INSTALLED_APPS:
        ‘django.contrib.sessions’
    MIDDLEWARE:
        ‘django.contrib.sessions.middleware.SessionMiddleware’
每个HttpResponse对象都有一个session属性，也是一个类字典对象 讲解cookie和session通信，session_id等

#### 3.常用操作
- get(key, default=None) 根据键获取会话的值 
- clear() 清除所有会话 
- flush() 删除当前的会话数据并删除会话的cookie 
- delete request[‘session_id’] 删除会话 
- session.session_key 获取session的key 设置数据 
- request.session[‘user’] = username 数据存储到数据库中会进行编码使用的是base64 

>注意: Session 支持中文 cookie不支持中文 token自己维护