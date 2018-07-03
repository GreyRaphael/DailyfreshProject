from django.db import models


# Create your models here.
class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    # sha1 length=40
    upwd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=30)
    # default是给python用的, 不是给数据库用的, 不需要migration
    # blank, null是数据库层面的，需要migration
    ureceiver = models.CharField(max_length=20, default='')
    uaddr = models.CharField(max_length=100, default='')
    uzipcode = models.CharField(max_length=6, default='')
    uphone = models.CharField(max_length=11, default='')
