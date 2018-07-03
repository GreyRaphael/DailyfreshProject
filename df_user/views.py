from django.shortcuts import render, redirect
from .models import *
import hashlib
from django.http import JsonResponse, HttpResponseRedirect


# Create your views here.
def register(request):
    context = {'title': '注册'}
    return render(request, 'register.html', context)


def register_handle(request):
    # get the form
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    ucpwd = post.get('cpwd')
    uemail = post.get('email')

    # 判断两个密码，虽然js已经判断过了
    if upwd != ucpwd:
        return redirect('/user/register')

    # encrypt pwd
    m = hashlib.sha1()
    m.update(bytes(upwd, 'utf8'))
    encrypt_pwd = m.hexdigest()

    # create UserInfo object
    user = UserInfo()
    user.uname = uname
    user.upwd = encrypt_pwd
    user.uemail = uemail
    user.save()

    # register success to redirect /user/login
    return redirect('/user/login')


def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


def login(request):
    uname = request.COOKIES.get('uname', '')
    # 后面三个是给login_handle用的
    context = {'title': '天天生鲜-登录', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'login.html', context)


def login_handle(request):
    # get the form
    post = request.POST
    uname = post.get('username')
    upwd = post.get('upwd')
    cb_flag = post.get('cb_flag', 0)

    users = UserInfo.objects.filter(uname=uname)
    if len(users) == 1:
        # compared encrypt pwd
        m = hashlib.sha1()
        m.update(bytes(upwd, 'utf8'))
        encrypt_pwd = m.hexdigest()
        if encrypt_pwd == users[0].upwd:
            red = HttpResponseRedirect('/user/info/')
            if cb_flag != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {
                'title': '用户登录',
                'error_name': 0,
                'error_pwd': 1,
                'uname': uname,
                'upwd': upwd,
            }
            return render(request, 'login.html', context)
    else:
        context = {
            'title': '用户登录',
            'error_name': 1,
            'error_pwd': 0,
            'uname': uname,
            'upwd': upwd,
        }
        return render(request, 'login.html', context)


def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    context = {
        'title': '用户中心',
        'user_email': user_email,
        'user_name': request.session['user_name']
    }
    return render(request, 'user_center_info.html', context)
