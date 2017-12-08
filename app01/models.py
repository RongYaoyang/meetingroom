from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=32,verbose_name='用户名')
    pwd = models.CharField(max_length=32,verbose_name='密码')

    def __str__(self):
        return self.name


class TalkRoom(models.Model):
    title = models.CharField(max_length=32,verbose_name='会议室名')

    def __str__(self):
        return self.title


class Date(models.Model):
    date = models.CharField(max_length=32,verbose_name='日期时间年月日表示')
    time = models.CharField(max_length=32,verbose_name='开会时间小时表示')
    talkroom = models.ManyToManyField(to='TalkRoom',verbose_name='预定会议室',related_name='date_talkroom')
    user = models.ManyToManyField(to='User', verbose_name='预定用户', related_name='user_date')

    def __str__(self):
        return self.date + self.time


class Time(models.Model):
    '''生成表头用'''
    title = models.CharField(max_length=32,verbose_name='开会时间小时表示')

    def __str__(self):
        return self.title