from django.db import models

'''用户表'''
class User(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=128, primary_key=True)
    password = models.CharField(verbose_name="密码", max_length=256)
    #email = models.EmailField(verbose_name="邮箱", unique=True)
    c_time = models.DateTimeField(auto_now_add=True)
