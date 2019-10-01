from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Article(models.Model):

    title = models.CharField(max_length=30)

    content = models.TextField()

    # created_time =models.DateField(default=timezone.now)
    created_time =models.DateTimeField(auto_now_add=True)

    last_updated_time = models.DateTimeField(auto_now=True)

    autor = models.ForeignKey(User,on_delete=models.DO_NOTHING,default=1)

    is_deleted = models.BooleanField(default=False)

    read_num = models.IntegerField(default=0)
    # def __str__(self):
    #     return '<Article:%s>'% self.title

