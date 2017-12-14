# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from df_goods.models import TypeInfo, GoodsInfo


def index(request):
    typelist = TypeInfo.objects.all()
    type00 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    type10 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type11 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    type20 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type21 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    type30 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type31 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    type40 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type41 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    type50 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type51 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    context = {'type00': type00,
               'type01': type01,
               'type10': type10,
               'type11': type11,
               'type20': type20,
               'type21': type21,
               'type30': type30,
               'type31': type31,
               'type40': type40,
               'type41': type41,
               'type50': type50,
               'type51': type51,
               }
    return render(request,'df_goods/index.html',context)
