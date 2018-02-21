# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class CartInfo(models.Model):
    """数据库设计
        1.user和goods的关系是M:N,类比于银行用户和交易类型
        2.选定三个字段 ，用户 商品 购买数量，类比 DDTNJNP:DD transaction history journal file
    """

    # 外键：调用其他应用的模型类:应用名.模型类
    user = models.ForeignKey("df_user.UserInfo")
    goods = models.ForeignKey("df_goods.GoodsInfo")
    count = models.IntegerField()
    def __str__(self):
        return self.user.uname.encode('utf-8')