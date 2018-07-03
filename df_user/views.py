from django.shortcuts import render, redirect
from .models import *
import hashlib


# Create your views here.
def register(request):
    return render(request, 'register.html')


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
