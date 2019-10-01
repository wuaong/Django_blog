from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404

from blog.models import Blog, BlogType
from blog.utils import get_blog_list_common_data, read_statistics_once_read
from read_statistics.models import ReadNum


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context=get_blog_list_common_data(request,blogs_all_list)

    context['title'] = 'blog_list'

    return render(request, 'blog/blog_list.html', context=context)


def blogs_with_type(request,blog_type_id):
    blog_type = get_object_or_404(BlogType, pk=blog_type_id)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request,blogs_all_list)

    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context=context)


def blogs_with_date(request,year,month):

    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    context = get_blog_list_common_data(request,blogs_all_list)
    blogs_with_date = '%s年%s月'% (year,month)

    context['blog_with_date'] =blogs_with_date
    return render(request, 'blog/blogs_with_dates.html', context=context)


def blog_detail(request,blog_id):

    blog = get_object_or_404(Blog,pk=blog_id)

    key = read_statistics_once_read(request, blog)

    previous_blog = Blog.objects.filter(created_time__gt=blog.created_time).last()
    next_blog = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context = {
        'blog':blog,
        'previous_blog':previous_blog,
        'next_blog':next_blog
    }

    response=render(request, 'blog/blog_detail.html', context=context)
    response.set_cookie(key,'true')
    return response