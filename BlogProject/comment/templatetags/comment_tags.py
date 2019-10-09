from django import template
from django.contrib.contenttypes.models import ContentType

from comment.forms import CommentForm
from comment.models import Comment

register = template.Library()

@register.simple_tag
def get_comment_count(obj):
    content_type=ContentType.objects.get_for_model(obj)
    comment_count=Comment.objects.filter(content_type=content_type,object_id=obj.id).count()

    return comment_count

@register.simple_tag
def get_comment_form(obj):
    content_type=ContentType.objects.get_for_model(obj)
    form=comment_form = CommentForm(initial={
                   'content_type':content_type,'object_id':obj.id,'reply_comment_id':0})
    return form


@register.simple_tag()
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments =Comment.objects.filter(content_type=content_type,object_id=obj.id,root=None)
    return comments.order_by('-comment_time')