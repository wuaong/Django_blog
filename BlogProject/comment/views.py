from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from comment.forms import CommentForm
from comment.models import Comment


def update_comment(request):

    '''referer = request.META.get('HTTP_REFERER', reverse('home'))

    if not request.user.is_authenticated:
        return render(request, 'error.html', {'message': '用户未登录','redirect_to':referer})
    text = request.POST.get('text','').strip()
    if text == '':
        return render(request, 'error.html', {'message': '评论内容为空','redirect_to':referer})
    try:
        content_type = request.POST.get('content_type', '')
        object_id = int(request.POST.get('object_id', ''))
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = model_class.objects.get(id=object_id)
    except Exception as e:
        return render(request, 'error.html', {'message': '评论对象不存在','redirect_to':referer})

    comment = Comment()
    comment.text =text
    comment.user =request.user
    comment.content_object=model_obj
    comment.save()
    return redirect(referer)'''

    referer = request.META.get('HTTP_REFERER', reverse('home'))
    data ={}
    if request.method == 'POST':
        comment_form = CommentForm(request.POST,user=request.user)
        if comment_form.is_valid():
            comment = Comment()
            comment.text = comment_form.cleaned_data['text']
            comment.user = comment_form.cleaned_data['user']
            comment.content_object = comment_form.cleaned_data['content_object']

            parent = comment_form.cleaned_data['parent']
            if not parent is None:   #回复
                comment.root = parent.root if not parent.root is None else parent
                comment.parent=parent
                comment.reply_to=parent.user
            comment.save()
            #发送邮件通知
            comment.send_emial()


            data['status'] ="SUCCESS"
            data['username'] = comment.user.username
            data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
            data['text'] = comment.text
            if not parent is None:
                data['reply_to'] = comment.reply_to.username
            else:
                data['reply_to'] = ''
            data['pk'] = comment.pk
            data['root_pk'] = comment.root.pk if not comment.root is None else ''
        else:
            # return render(request, 'error.html', {'message': comment_form.errors,'redirect_to':referer})
            data['status'] = "ERROR"
            data['message'] = list(comment_form.errors.values())[0][0]

        return JsonResponse(data)
