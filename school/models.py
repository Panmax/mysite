# -*- coding: utf-8 -*
from django.db import models
from django.contrib.auth.models import User


class Publish(models.Model):
    sex = models.IntegerField()#1男2女3不限4公告
    college = models.IntegerField()#1科信2主校3西校4中华南5丛台校区6邯郸学院7邯郸大学8公告
    publisher = models.ForeignKey(User, related_name='publisherid')
    accepter = models.ForeignKey(User,null=True,blank=True,related_name='accepterid')
    date = models.DateField()
    publishDate = models.DateField(auto_now=True, auto_now_add=True)
    price = models.FloatField()
    time = models.IntegerField() #6公告
    other = models.CharField(max_length=200,  blank=True)
    state = models.IntegerField(default=3)#0删除 1过期 2接受 3激活 4公告
    def __unicode__(self):
        return unicode(self.publisher)
