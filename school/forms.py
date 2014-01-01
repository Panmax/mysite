# -*- coding: utf-8 -*
from django import forms
from django.forms import ModelForm

class UserLoginForm(forms.Form):
    phoneNumber = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':"手机号/邮箱"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':"密码"}))

class UserRegistForm(forms.Form):
    phoneNumber = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':"手机号"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':"邮箱"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':"密码"}))
    repassword = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':"重复密码"}))

class PublishForm(forms.Form):
    SEX_CHOICES =(('0', '所需性别？'),('1','我要找汉子',),('2','我需要妹纸',),('3','男女都可以，爷不在乎'))
    TIME_CHOICES = (('0', '哪节课？'),('1','上午--第一大节'),('2','上午--第二大节'),('3','下午--第一大节'),('4','下午--第二大节'),('5','晚上--要加薪哦'))
    COLLEGE_CHOICES = (('0', '在哪个校区上课？'),('1','东校区'),('2','主校区'),('3','西校区'),('4','中华南校区'),('5', '丛台校区'),('6', '邯郸学院'), ('7', '邯郸大学'))
    sex = forms.ChoiceField(label='',widget=forms.Select(attrs={'class':'form-control'}), choices=SEX_CHOICES)
    college =  forms.ChoiceField(label='',widget=forms.Select(attrs={'class':'form-control'}), choices=COLLEGE_CHOICES)
    date = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':"上课日期，如： 2013-11-01"}))
    time = forms.ChoiceField(label='',widget=forms.Select(attrs={'class':'form-control'}), choices=TIME_CHOICES)
    price = forms.FloatField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':"酬金（单位/元）"}))
    other = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':"（选填）其它要求，如：帮我做好课堂笔记；禁止与我们班女生调情……", 'rows':"3"}), required=False)