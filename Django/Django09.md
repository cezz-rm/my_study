# restful操作实例

## 1.修改响应的结构
修改settings.py文件中的返回数据结构的配置信息

	# 配置restful api返回结果
	REST_FRAMEWORK = {
	    # 分页
	    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
	    'PAGE_SIZE': 2,
	    # 设置搜索
	    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',
	                                'rest_framework.filters.SearchFilter'),
	    # 返回结构自定义
	    'DEFAULT_RENDERER_CLASSES': (
	        'utils.renderResponse.CustomJsonRenderer',
	    )
	}

## 2.重构JSONRenderer下的render方法
在utils文件下新建renderResponse文件，写一个类重构返回json数据的格式

	
	from rest_framework.renderers import JSONRenderer
	
	
	class CustomJsonRenderer(JSONRenderer):
	
	    def render(self, data, accepted_media_type=None, renderer_context=None):
	        if renderer_context:
	            if isinstance(data, dict):
	                msg = data.pop('msg', '请求成功')
	                code = data.pop('code', 0)
	            else:
	                msg = '请求成功'
	                code = 0
	            response = renderer_context['response']
	            response.status_code = 200
	            res = {
	                'code': code,
	                'msg': msg,
	                'data': data
	            }
	            return super().render(res, accepted_media_type, renderer_context)
	
	        else:
	            return super().render(data, accepted_media_type, renderer_context)

## 3.创建url
修改项目下的urls.py文件
	
	from stu import views
	from rest_framework.routers import SimpleRouter
	
	router = SimpleRouter()
	router.register(r'^student', views.StudentEdit)
	
	urlpatterns = [
	    url(r'index/', login_required(views.index)),
	    url(r'addstu/', login_required(views.addStu), name='add'),
	    url(r'addinfo/(?P<stu_id>\d+)/', login_required(views.addStuInfo), name='addinfo'),
	]	
	
	urlpatterns += router.urls

## 4.创建serializer_class
在项目下的views.py文件下
	
	from stu.serializers import StudentSerializer
	from rest_framework import mixins, viewsets

	class StudentEdit(mixins.ListModelMixin,
	                  mixins.RetrieveModelMixin,
	                  mixins.UpdateModelMixin,
	                  mixins.DestroyModelMixin,
	                  mixins.CreateModelMixin,
	                  viewsets.GenericViewSet):
	
	    # 查询所有信息
	    queryset = Student.objects.all()
	    # 序列化
	    serializer_class = StudentSerializer
	    # 过滤
	    filter_class = StuFilter
	
	    # 定义一个方法排序
	    def get_queryset(self):
	        query = self.queryset
	        return query.filter(s_delete=0).order_by('-id')
	
	    # 软删除，重构删除方法
	    def destroy(self, request, *args, **kwargs):
	        instance = self.get_object()
	        instance.s_delete = 1
	        instance.save()
	        return Response({'msg': '删除成功'})

## 5.定义serializer
在项目下新建一个serizlizers.py文件

	
	from rest_framework import serializers
	
	from stu.models import Student
	from uauth.models import Users
	
	
	class StudentSerializer(serializers.ModelSerializer):
	
	    s_name = serializers.CharField(error_messages={
	        'blank': '用户名不能为空',
	        'max_length': '用户名不能超过10个字符',
	        'min_length': '用户名至少为2个字符'
	    }, max_length=10, min_length=2)
	    s_tel = serializers.CharField(error_messages={
	        'blank': '电话不能为空'
	    })
	
	    class Meta:
	        model = Student
	        fields = ['id', 's_name', 's_tel', 's_yunwen', 's_operate_time', 's_status']
	        # 显示外键的所有字段
	        # depth = 1
	        # 除了某个字段其他的都显示
	        # exclude = ['c_num']
	
	    def to_representation(self, instance):
	
	        data = super().to_representation(instance)
	        try:
	            data['s_addr'] = instance.studentinfo.i_addr
	        except Exception as e:
	            data['s_addr'] = ''
	        # 将英文转为中文
	        data['s_status'] = dict(Student.STATUS)[data['s_status']]
	        #data['s_status'] = dict(Student.STATUS).pop(data['s_status'])
	        return data

## 6.定义filters
在项目下新建一个filters.py文件

	
	import django_filters
	from rest_framework import filters
	
	from stu.models import Student
	
	
	class StuFilter(filters.FilterSet):
	
	    name = django_filters.CharFilter('s_name', lookup_expr='icontains')
	    tel = django_filters.CharFilter('s_tel')
	    status = django_filters.CharFilter('s_status')
	    operate_time_min = django_filters.DateTimeFilter('s_operate_time', lookup_expr='gt')
	    operate_time_max = django_filters.DateTimeFilter('s_operate_time', lookup_expr='lt')
	    yuwen_min = django_filters.NumberFilter('s_yunwen', lookup_expr='gte')
	    yuwen_max = django_filters.NumberFilter('s_yunwen', lookup_expr='lte')
	
	    class Meta:
	        model = Student
	        fields = ['s_name', 's_tel', 's_status', 's_operate_time', 's_yunwen']


## 7.使用ajax请求获取数据
	
	$(function (){
		$('#load').on('click', function(){
			$.get({
            })
		    $.ajax({
				type: 'get',
				url: 'http://127.0.0.1:8000/stu/student/',
				dataType: 'json',
				error: function(){
					alert('服务器不堪重负！')
				},
				success: function(obj){
					for(var i = 0; i < obj.length; i++){
						{#var stu = obj[i].s_name#}
                        {#var tel = obj[i].s_tel#}
						{#$('#stu_info').append(stu, tel, $('<p>'));#}
                        var info = $('<p>').text(obj[i].s_name + '...' +obj[i].s_tel)
                        $('#stu_info').append(info)
					}
				}
			});
		});
	});

>>注：本文中使用到的两个model表如下

	class Student(models.Model):
	    s_name = models.CharField(max_length=10)
	    s_tel = models.CharField(max_length=11)
	    s_yunwen = models.DecimalField(max_digits=3, decimal_places=1, null=True)
	    s_operate_time = models.DateTimeField(null=True, auto_now=True)
	    STATUS = [
	        ('NONE', '正常'),
	        ('NEXT_SCH', '留级'),
	        ('DROP_SCH', '退学'),
	        ('LEAVE_SCH', '休学')
	    ]
	    s_status = models.CharField(choices=STATUS, max_length=10, default='NONE')
	    s_delete = models.BooleanField(default=0)
	
	    class Meta:
	        db_table = 'stu'
	
	
	class StudentInfo(models.Model):
	    i_addr = models.CharField(max_length=30)
	    i_image = models.ImageField(upload_to='upload', null=True)
	    s = models.OneToOneField(Student)
	
	    class Meta:
	        db_table = 'stu_info'