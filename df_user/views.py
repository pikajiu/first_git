# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from df_goods.models import GoodsInfo
from df_user.models import UserInfo
from hashlib import sha1
import user_check_decorator


def register(request):
    return render(request, 'df_user/register.html')


def register_handle(request):
    # 接收用户输入,最好直接复制每个html标签的name属性
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    if upwd != upwd2:
        return redirect('/user/register/')
    # 加密
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()
    # 创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    return redirect('/user/login/')


def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


def login(request):
    cookies = request.COOKIES
    # 1. get cookie,need default value to avoid 'NONE'.
    uname = request.COOKIES.get('user_account', '')
    # 2. fill in the account blank
    context = {'error_name': 0, 'error_pwd': 0, 'username': uname}
    return render(request, 'df_user/login.html', context)


def login_handle(request):
    # 1. get account & password
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    remember = post.get('remember', 0)
    # 2. validate account if it has existed,yes -- return .
    usercount = UserInfo.objects.filter(uname=uname)
    # if account exist in database
    if (len(usercount) > 0):
        s1 = sha1()
        s1.update(upwd)
        upwd2 = s1.hexdigest()
        # 3. validate password : compare with database password after sha1.if not, return .
        # check whether password is correct
        if upwd2 == usercount[0].upwd:
            url = request.COOKIES.get('url', '/index/')
            redirect_to_info = HttpResponseRedirect(url)
            # # # add a new function: Remember account name
            #     随便传个值，就不会是0
            if remember != 0:
                # 1.set cookie,return cookie to redirect
                redirect_to_info.set_cookie('user_account', uname)
            else:
                redirect_to_info.set_cookie('username', '', max_age=-1)
            request.session['user_id'] = usercount[0].id
            request.session['user_name'] = usercount[0].uname
            # 4. validate successful. redirect to user_info
            return redirect_to_info
        else:
            # password error
            # context = {'error_name': 0, 'error_pwd': 1}  多挖两个坑
            context = {'error_name': 0, 'error_pwd': 1, 'username': uname, 'password': upwd}
            return render(request, 'df_user/login.html', context)
    else:
        # account not exist
        # context = {'error_name': 1, 'error_pwd': 0} 多挖两个坑
        context = {'error_name': 1, 'error_pwd': 0, 'username': uname, 'password': upwd}

        return render(request, 'df_user/login.html', context)


def logout(request):
    request.session.flush()
    return redirect('/index/')


@user_check_decorator.login
def user_info(request):
    user = UserInfo.objects.get(id=request.session['user_id'])

    # 通过cookie拿到user的浏览记录，安全考虑应换成session
    scan_list = request.COOKIES.get('scan_list','')
    scan_lists = scan_list.split(',')
    goods_list = []
    for goods in scan_lists:
        goods_list.append(GoodsInfo.objects.get(id = int(goods)))
    content = {
        'user':user,
        'goods_list':goods_list,
    }
    return render(request, 'df_user/user_center_info.html',content)


@user_check_decorator.login
def user_order(request):
    return render(request, 'df_user/user_center_order.html')


@user_check_decorator.login
def user_site(request):
    # get user info from database
    user = UserInfo.objects.get(id=request.session['user_id'])
    # if submit ，get user additional info from form
    if request.method == 'POST':
        post = request.POST
        user.ushou = post['ushou']
        user.uaddress = post['uaddress']
        user.uyoubian = post['uyoubian']
        user.uphone = post['uphone']
        user.save()
    # need variable to receive them in template
    context = {'user': user}
    return render(request, 'df_user/user_center_site.html', context)
