# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from Queue import Queue

from django.core.paginator import Paginator
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
    return render(request, 'df_goods/index.html', context)


def list(request, typeID, pagenum, sortType):
    # 事先声明，解决局部变量未定义问题
    news = []
    true_typeid = int(typeID)
    typeinfo = TypeInfo.objects.get(id=(true_typeid))
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    if sortType == '1':  # 默认排序方式，最新
        goods_list = GoodsInfo.objects.filter(gtype_id=int(true_typeid)).order_by('-id')
    if sortType == '2':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(true_typeid)).order_by('-gprice')
    if sortType == '3':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(true_typeid)).order_by('-gclick')

    paginator = Paginator(goods_list, 10)
    page = paginator.page(int(pagenum))
    context = {
        'page': page,
        'paginator': paginator,
        'typeinfo': typeinfo,
        'sort': sortType,
        'news': news,
    }

    return render(request, 'df_goods/list.html', context)


def detail(request, gid):
    goods = GoodsInfo.objects.get(pk=int(gid))
    goods.gclick += 1
    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {
        'title': goods.gtype.ttitle, 'g': goods, 'news': news, 'id': gid
    }
    response = render(request, 'df_goods/detail.html', context)

    # 取得Cookie值
    scan_list = request.COOKIES.get('scan_list', '')
    goods_id = '%d'%goods.id
    if scan_list != '':

        # 拆分成列表
        scan_lists = scan_list.split(',')
        if scan_lists.count(goods_id)>0:
            scan_lists.remove(goods_id)
        scan_lists.insert(0,goods_id)
        if len(scan_lists)>5:
            del scan_lists[5]
        scan_list = u','.join(scan_lists)
    else:
        scan_list = goods_id
    response.set_cookie('scan_list',scan_list)


    return response
