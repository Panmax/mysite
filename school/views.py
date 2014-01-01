# -*- coding: utf-8 -*
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from school.forms import *
from re import match,compile
from school.models import Publish
from django.contrib.auth.models import User
from django.contrib import auth

from datetime import  datetime,timedelta


def index(request):
    errors=[]
    if request.method == 'POST':
        login = UserLoginForm(request.POST)
        if not request.POST.get('phoneNumber',''):
            errors.append('手机号不能为空！')
        if not request.POST.get('password',''):
            errors.append("密码不能为空！")
        if errors:
            return render_to_response('index.html', {'login': login, 'errors': errors})

        if login.is_valid():
            phoneNumber = login.cleaned_data['phoneNumber']
            password = login.cleaned_data['password']
            #这是之前我自己建的user，已弃用
            #users = User.objects.filter(username = phoneNumber, password = password)|User.objects.filter(email = phoneNumber, password = password)
            #同时尝试手机号和邮箱来获取用户信息
            user = auth.authenticate(username=phoneNumber, password=password)
            print phoneNumber
            print password
            print user
            if not user:
                try:
                    phoneNumber = User.objects.get(email=phoneNumber).username
                    user = auth.authenticate(username=phoneNumber, password=password)
                except:
                    pass

            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('')
            else:
                errors.append("帐号或密码错误")
                return render_to_response('index.html', {'login': login, 'errors': errors, 'path':'index'})
    else:
        login = UserLoginForm()
        if request.user.is_authenticated():
            return render_to_response('index.html', {'phoneNumber': request.user.username, 'login':login, 'path':'index'})
        else:
            return render_to_response('index.html', {'phoneNumber': '', 'login':login, 'path':'index'})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def registPage(request):
    errors=[]
    if request.method == 'POST':
        regist = UserRegistForm(request.POST)
        if not request.POST.get('phoneNumber',''):
            errors.append('手机号不能为空！')
        else:
            pattern = compile(r'^[1][358]\d{9}$')
            if not pattern.match(request.POST.get('phoneNumber','')):
                errors.append("手机号码有误！")
        password = request.POST.get('password','')
        repassword =  request.POST.get('repassword', '')

        if not request.POST.get('email', ''):
            errors.append("邮箱不能为空！")
        elif regist['email'].errors:
            errors.append("邮箱格式不正确！")

        if not password:
            errors.append("密码不能为空！")
        elif not repassword:
            errors.append("重复密码不能为空！")
        elif password != repassword:
            errors.append("两次密码不同！")
        elif not 6 <= len(password) <= 20:
            errors.append("密码长度为6-20位")

        if errors:
            return render_to_response('regist.html', {'regist': regist, 'errors': errors})

        if regist.is_valid():
            phoneNumber = regist.cleaned_data['phoneNumber']
            password = regist.cleaned_data['password']
            email = regist.cleaned_data['email']
            if User.objects.filter(username=phoneNumber):
                errors.append("该手机号已存被注册！")
                return render_to_response('regist.html', {'regist': regist, 'errors': errors})
            elif User.objects.filter(email=email):
                errors.append("该邮箱已存被注册！")
                return render_to_response('regist.html', {'regist': regist, 'errors': errors})
            #User.objects.create(phoneNumber = phoneNumber, password = password, email = email)
            #request.session['phoneNumber'] = phoneNumber
            user = User.objects.create_user(username=phoneNumber,email=email,password=password)
            user.is_staff = True
            user.is_active=True
            user.save()
            user = auth.authenticate(username=phoneNumber,password=password)
            auth.login(request,user)
            return HttpResponseRedirect('/login/')
    else:
        regist = UserRegistForm()
        return render_to_response('regist.html',{'regist':regist})

def comming(request):
    if request.user.is_authenticated():
        phoneNumber = request.user.username
    path = request.path
    return render_to_response('comming.html', locals())

def publish(request):
    errors = []
    path = '/publish/'
    phoneNumber = ''
    if request.user.is_authenticated():
        phoneNumber = request.user.username
    if request.method == 'POST':
        publishForm = PublishForm(request.POST)
        if request.POST.get('sex') == '0':
            errors.append("请选择性别！")
        if request.POST.get('college') == '0':
            errors.append("请选择所在校区！")
        if not request.POST.get('date',''):
            errors.append("未填写上课日期")
        elif publishForm['date'].errors:
            errors.append("请按照：年-月-日 的格式输入日期！")
        if request.POST.get('time') == '0':
            errors.append("请选择节次")
        if not request.POST.get('price', ''):
            errors.append("佣金不能为空")
        elif publishForm['price'].errors :
            errors.append("佣金必须为大于等于零的数字！")
        if len(request.POST.get('other','')) > 200:
            errors.append("其它要求不能超过200字！")
        if errors:
            return render_to_response("publish.html", locals())

        if publishForm.is_valid:
            publisher = User.objects.get(username = phoneNumber)
            sex=publishForm.cleaned_data['sex']
            date=publishForm.cleaned_data['date']
            college = publishForm.cleaned_data['college']

            now = (datetime.now()).date()
            if date<now:
                errors.append("日期有误！抱歉，我们不能穿越~")
                return render_to_response("publish.html", locals())

            if date > (now + timedelta(days=7)):
                errors.append("只能发布一周内的任务哦~")
                return render_to_response("publish.html", locals())

            time=publishForm.cleaned_data['time']
            price=publishForm.cleaned_data['price']
            if price<0:
                errors.append("佣金必须为大于等于零的数字！")
                return render_to_response("publish.html", locals())
            other=publishForm.cleaned_data['other']
            if not Publish.objects.filter(sex=sex,college=college,date=date, time=time,price=price,other=other,publisher=publisher):
                result=Publish.objects.create(sex=sex,college=college,date=date, time=time,price=price,other=other,publisher=publisher)
                result.save()
            return HttpResponseRedirect('/publish/success')
    else:
        publishForm = PublishForm()
        return render_to_response("publish.html",locals())

def receive(request,offset=''):
    try:
        offset = int(offset)
    except ValueError:
         return HttpResponseRedirect('/receive/1/')
    path = '/receive/'
    phoneNumber = ''
    if request.user.is_authenticated():
        phoneNumber = request.user.username
    #计算所有满足条件的数量
    count = (Publish.objects.filter(state=1) | Publish.objects.filter(state=2)| Publish.objects.filter(state=3) | Publish.objects.filter(state=4)).count()
    #产生的页数为范围（不包括下届），最后一页为(count-1)/10+2
    pages = range(1,(count-1)/10+2)
    #判断获取的页码是否大于一共的页数
    if offset not in pages:
        return HttpResponseRedirect('/receive/1/')
    #检测过期任务
    testPublishs = Publish.objects.filter(state=3)

    if testPublishs:
        now = (datetime.now()).date()
        for testPublish in testPublishs:
            if testPublish.date < now:
                testPublish.state = 1
                testPublish.save()

    page1 = (offset-1)*10
    page2 = offset*10
    publishs = (Publish.objects.filter(state=1) | Publish.objects.filter(state=2)| Publish.objects.filter(state=3) | Publish.objects.filter(state=4)).order_by("-state","-publishDate", "-date", "-price")[page1:page2]

    return render_to_response("receive.html", locals())


def success(request):
    phoneNumber = ''
    if request.user.is_authenticated():
        phoneNumber = request.user.username
    return render_to_response("success.html", locals())

def select(request,id):
    errors = []
    phoneNumber = ''
    if request.user.is_authenticated():
        phoneNumber = request.user.username
    if phoneNumber:
        try:
            id = int(id)
        except ValueError:
            errors.append("系统异常，请正确操作。")
            return render_to_response("select_result.html", locals())
        try:
            getInfo = Publish.objects.get(id = id)
        except:
            errors.append("系统异常，请正确操作。")
            return render_to_response("select_result.html", locals())
        user = User.objects.get(username=phoneNumber)
        if getInfo.publisher == user:
            errors.append("请不要领取自己发布的任务！")
            return render_to_response("select_result.html", locals())

        if getInfo.state == 3:
            getInfo.state=2
            getInfo.accepter = user
            getInfo.save()
            return render_to_response("select_result.html", locals())
        elif getInfo.state == 2:
            errors.append("你下手太慢了，")
            errors.append("这个任务已经被别人抢走了！")
            return render_to_response("select_result.html", locals())
        else:
            errors.append("这个任务不存在！")
            return render_to_response("select_result.html", locals())
    else:
        return render_to_response("select_result.html", locals())

def task(request):
    phoneNumber = ''
    if request.user.is_authenticated():
        phoneNumber = request.user.username
    if phoneNumber:
        #检测过期任务
        testPublishs = Publish.objects.filter(state=3)
        if testPublishs:
            now = (datetime.now()).date()
            for testPublish in testPublishs:
                if testPublish.date < now:
                    testPublish.state = 1
                    testPublish.save()
        publishs = Publish.objects.filter(publisher=request.user).order_by("-publishDate")
        accepts = Publish.objects.filter(accepter = request.user).order_by("-publishDate")
        return render_to_response("task.html", locals())
    else:
        return render_to_response("task.html", locals())

def delete(request, id):
    phoneNumber = ''
    if request.user.is_authenticated():
        phoneNumber = request.user.username
    errors = []
    try:
        id = int(id)
    except ValueError:
        errors.append("系统异常，请正确操作。")
        return render_to_response("select_result.html", locals())
    try:
        getInfo = Publish.objects.get(id = id)
    except:
        errors.append("系统异常，请正确操作。")
        return render_to_response("select_result.html", locals())
    user = User.objects.get(username=phoneNumber)
    if getInfo.publisher == user:
        getInfo.state = 0
        getInfo.save()
        return HttpResponseRedirect('/task/')
    else:
        errors.append("只能删除自己发布的任务！")
        return render_to_response("select_result.html", locals())

def help(request):
    phoneNumber = ''
    if request.user.is_authenticated():
        phoneNumber = request.user.username
    path = '/help/'
    return render_to_response("help.html", locals())



