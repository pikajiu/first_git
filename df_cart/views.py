# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse

from df_cart.models import CartInfo
from django.shortcuts import render

from df_goods.models import GoodsInfo
from df_user import user_check_decorator
from df_user.models import UserInfo


@user_check_decorator.login
def cart(request):
    user_id = request.session.get('user_id')

    cart_list = CartInfo.objects.filter(user=user_id)
    context = {
        'user': user_id,
        'cart_list': cart_list,
    }
    return render(request, 'df_cart/cart.html', context)


@user_check_decorator.login
def add(request, goods_id, count):
    user_id = request.session['user_id']
    user = UserInfo.objects.get(id=user_id)
    goods_id = int(goods_id)
    goods = GoodsInfo.objects.get(pk=goods_id)
    count = int(count)
    carts = CartInfo.objects.filter(user=user, goods=goods)

    # 修改
    if len(carts) > 0:
        cart = carts[0]
        cart.count += count
    # 新增
    else:
        cart = CartInfo()
        """ValueError: Cannot assign "6": "CartInfo.user" must be a "UserInfo" instance."""
        # cart.user = user_id
        cart.user = user
        """ValueError: Cannot assign "11": "CartInfo.goods" must be a "GoodsInfo" instance.
            这个字段都是外键定义，要传object       
        """
        cart.goods = goods

        cart.count = count
    cart.save()

    if request.is_ajax():
        count = CartInfo.objects.filter(user=user_id).count()
    return JsonResponse({'count': count})


@user_check_decorator.login
def edit(request, cart_id, count):
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        count1 = cart.count = count
        cart.save()
        data = {'result': 0}
    except Exception as e:
        data = {'result': count1}
    return JsonResponse(data)


@user_check_decorator.login
def delete(request, cart_id):
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data = {'result': 0}
    except Exception as e:
        data = {'result': -1}
    finally:
        return JsonResponse(data)
