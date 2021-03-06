import threading

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string

from BlogProject import settings


class SendEmail(threading.Thread):
    def __init__(self,subject, text, email, fail_silently=False):
        self.subject = subject
        self.text =text
        self.email =email
        self.fail_silently=fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.subject,'',
                  settings.EMAIL_HOST_USER, [self.email],
                  fail_silently=self.fail_silently
                  ,html_message=self.text)

class Comment(models.Model):

    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,related_name='comments',on_delete=models.CASCADE)

    root = models.ForeignKey('self',related_name='root_comment',null=True,on_delete=models.CASCADE)
    parent = models.ForeignKey('self',related_name='parent_comment',null=True,on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User,related_name='replies',null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    def send_emial(self):
        if self.parent is None:
            #评论我的博客
            subject ='有人评论我的博客'
            email = self.content_object.get_email()
        else:
            #回复评论
            subject = '有人回复你的评论'
            email = self.reply_to.email
        if email != '':
            context ={
                'comment_text':self.text,
                'url':self.content_object.get_url()
            }
            text = render_to_string('comment/send_email.html',context=context)
            send_mail=SendEmail(subject, text, email)  #运用多线程
            send_mail.start()

    class Meta:
        ordering = ['comment_time']