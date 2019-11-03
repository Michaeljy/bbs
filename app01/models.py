from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserInfo(AbstractUser):
    phone = models.BigIntegerField(null=True)
    avatar = models.FileField(
        upload_to='avatar/', default='avatar/default.png'
    )
    create_time = models.DateTimeField(auto_now_add=True)

    blog = models.OneToOneField(to='Blog',null=True)


class Blog(models.Model):
    site_name = models.CharField(max_length=32)
    site_title = models.CharField(max_length=32)
    site_theme = models.CharField(max_length=64)


class Category(models.Model):
    name = models.CharField(max_length=32)
    blog = models.ForeignKey(to='Blog', null=True)

class Tag(models.Model):
    name = models.CharField(max_length=32)
    blog = models.ForeignKey(to='Blog')


class Article(models.Model):
    name = models.CharField(max_length=32)
    desc = models.CharField(max_length=255)
    content = models.TextField()
    create_time = models.DateField(auto_now_add=True)

    comment_num = models.IntegerField()
    up_num = models.IntegerField()
    down_num = models.IntegerField()

    blog = models.ForeignKey(to='Blog', null=True)
    tags = models.ManyToManyField(to='Tag', through='Article2Tag', through_fields=('article', 'tag'))
    category = models.ForeignKey(to='Category', null=True)


class Article2Tag(models.Model):
    article = models.ForeignKey(to='Article', null=True)
    tag = models.ForeignKey(to='Tag', null=True)

class Comment(models.Model):
    user = models.ForeignKey(to='UserInfo', null=True)
    article = models.ForeignKey(to='Article', null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(to='self', null=True)
    content = models.CharField(max_length=255)


class UpAndDown(models.Model):
    user = models.ForeignKey(to='UserInfo', null=True)
    article = models.ForeignKey(to='Article', null=True)
    is_up = models.BooleanField()






