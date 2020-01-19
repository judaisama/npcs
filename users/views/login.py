from django.shortcuts import render
from users.models import User
from django.http import HttpResponseRedirect

def login(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        message = "所有字段都必须填写！"
        if username and password:  # 确保用户名和密码都不为空
            try:
                user = User.objects.get(username=username)
                if user.password == hash_code(password):
                    return render(request, 'analyse/home.html')
                else:
                    message = "密码不正确！"
            except:
                message = "用户名不存在！"
        return render(request, 'users/login.html', {"message": message})
    return render(request, 'users/login.html')


def register(request):
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username and password:
            try:
                User.objects.get(username=username)
                message = '用户名已存在！'
                return render(request, 'users/login.html', {'message': message})
            except:
                user = User(username=username, password=hash_code(password))
                user.save()
                message = '注册成功请登录！'
                return render(request, 'users/login.html', {'message': message})
    return render(request, 'users/login.html')


def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/')


def hash_code(s, salt='npcs'):
    import hashlib
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()
