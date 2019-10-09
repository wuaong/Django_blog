from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.shortcuts import render
from blog.models import Blog
from blog.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data, get_7_days_hot_data


def home(request):
    ct = ContentType.objects.get_for_model(Blog)
    dates,read_nums = get_seven_days_read_data(content_type=ct)
    today_hot_data =get_today_hot_data(content_type=ct)
    yesterday_hot_data =get_yesterday_hot_data(content_type=ct)

    #获取7天热门博客的缓存数据
    hot_data_with_7_days=cache.get('hot_data_with_7_days')
    if hot_data_with_7_days is None:
        hot_data_with_7_days = get_7_days_hot_data()
        cache.set('hot_data_with_7_days',hot_data_with_7_days,3600)

    hot_data_with_7_days=get_7_days_hot_data()
    context ={
        'dates':dates,
        'read_nums':read_nums,
        'today_hot_data':today_hot_data,
        'yesterday_hot_data':yesterday_hot_data,
        'hot_data_with_7_days':hot_data_with_7_days
    }
    return render(request,'home.html',context=context)


