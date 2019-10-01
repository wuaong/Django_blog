import datetime
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.http import request
from django.utils import timezone

from blog.models import BlogType, Blog
from read_statistics.models import ReadNum, ReadDetail

each_page_blogs_number = 5
def get_blog_list_common_data(request,blogs_all_list):
        paginator = Paginator(blogs_all_list,each_page_blogs_number) #每5页进行分页
        page_num = request.GET.get('page',1)
        page_of_blogs = paginator.get_page(page_num)
        current_page_num = page_of_blogs.number #获取当前页

        page_range=list(range(max(current_page_num-2,1),current_page_num))+\
                   list(range(current_page_num,min(current_page_num+2,paginator.num_pages)+1))

        #加上首页和尾页
        if page_range[0] !=1:
            page_range.insert(0,1)
        if page_range[-1] != paginator.num_pages:
            page_range.append(paginator.num_pages)

        blog_types = BlogType.objects.annotate(blog_count = Count('blog'))
        blog_dates = Blog.objects.dates('created_time', 'month', 'DESC')
        blog_dates_dict={}

        for blog_date in blog_dates:
            blog_count =Blog.objects.filter(created_time__year=blog_date.year,
                                            created_time__month= blog_date.month).count()
            blog_dates_dict[blog_date] = blog_count
        context = {
            'blogs': page_of_blogs.object_list,
            'page_of_blogs': page_of_blogs,
            'blog_types': blog_types,
            'pangiator': paginator,     #分液器
            'page_range': page_range,   #页码范围
            'blog_dates': blog_dates_dict
        }
        return context

def read_statistics_once_read(request,obj):

    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read"%(ct.model,obj.id)

    if not request.COOKIES.get(key):
        #总阅读数
        readnum,create = ReadNum.objects.get_or_create(content_type=ct,object_id=obj.id)
        readnum.read_num+=1
        readnum.save()

        #当天阅读数
        date = timezone.now().date()
        readDetail,create = ReadDetail.objects.get_or_create(content_type=ct,object_id=obj.id,date=date)
        readDetail.read_num+=1
        readDetail.save()
    return key

def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    read_nums = []
    for i in range(7,0,-1):
        date = today - datetime.timedelta(days=i)
        read_details = ReadDetail.objects.filter(content_type=content_type,date=date)
        result = read_details.aggregate(read_num_sum = Sum('read_num'))
        read_nums.append(result['read_num_sum'])
    return read_nums

