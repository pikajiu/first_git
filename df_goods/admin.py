# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from df_goods.models import TypeInfo, GoodsInfo


# class TypeInfoAdmin(admin.ModelAdmin):
#     list_select_related = ['id', 'ttitle']


# class GoodsInfoAdmin(admin.ModelAdmin):
#     list_per_page = 15
#     list_select_related = ['id', 'gtitle', 'gprice', 'gunit', 'gclick', 'gkucun', 'gcontent', 'gtype']


# admin.site.register(TypeInfo, TypeInfoAdmin)
# admin.site.register(GoodsInfo, GoodsInfoAdmin)
admin.site.register(TypeInfo)
admin.site.register(GoodsInfo)