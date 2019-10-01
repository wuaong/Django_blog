from django.http import HttpResponse, Http404
from django.shortcuts import render,get_object_or_404
from .models import Article

def article_detail(request,article_id):

    # article = Article.objects.get(pk=article_id)
    article = get_object_or_404(Article,pk=article_id)
    context ={
        'title' :'article_detail',
        'article':article,
    }

    return render(request,'article_detail.html',context=context)


def article_list(request):
    articles = Article.objects.filter(is_deleted=False)
    context ={
        'title':'article_title',
        'article_list':articles,
    }
    return render(request,'article_list.html',context=context)