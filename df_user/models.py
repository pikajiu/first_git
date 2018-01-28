# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# 数据驱动 先做model类
class UserInfo (models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=30)
    ushou = models.CharField(max_length=20,default='')
    uaddress = models.CharField(max_length=100,default='')
    uyoubian = models.CharField(max_length=6,default='')
    uphone = models.CharField(max_length=11,default='')
    #default, blank 是python层面的约束，不影响数据库，不需要重新迁移


    def __str__(self):
        return self.uname.encode('utf-8')