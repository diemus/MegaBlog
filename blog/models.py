from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name=models.CharField(max_length=32,unique=True)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    summary=models.TextField(max_length=200)
    content = models.TextField()
    publish_time = models.DateTimeField(auto_now_add=True)  # 第一次保存时自动添加时间
    modify_time = models.DateTimeField(auto_now=True)  # 每次保存自动更新时间
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    category = models.ForeignKey(to='Category',default='未分类')
    tags = models.ManyToManyField(to='Tag',blank=True)
    view_count = models.IntegerField(editable=False, default=0)
    STATUS = {
        0: '草稿',
        1: '发布',
        2: '删除',
    }
    status = models.SmallIntegerField(default=0, choices=STATUS.items())  # 0为草稿，1为发布，2为删除

    def __str__(self):
        return self.title

    def get_tags(self):
        return self.tags.all()

    def update_tags(self, tag_list):
        id_list=[]
        for tag in tag_list:
            obj,status=Tag.objects.get_or_create(name=tag)
            print(obj)
            id_list.append(obj.id)
        self.tags.set(id_list)

    # def remove_tags(self):
    #     self.tags.remove()

    class Meta:
        ordering = ['-publish_time']

class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    publish_Time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    content = models.TextField()
    root_id = models.IntegerField(default=0)  # 评论的最上层评论，若该评论处于最上层，则为0，
    parent_id = models.IntegerField(default=0)  # 评论的父评论，若无父评论，则为0

    def __str__(self):
        return self.content

class User(AbstractUser):
    name = models.CharField(max_length=12)
    avatar_path = models.ImageField(default="/static/image/avatar_default.jpg")

    def __str__(self):
        return self.name