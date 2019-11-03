from django.shortcuts import render, HttpResponse, reverse, redirect
from app01 import myforms
from app01 import models
from django.http import JsonResponse
from django.contrib import auth

# Create your views here.


def register(request):
    form_obj = myforms.MyRegForm() #生成空form对象
    if request.method == 'POST':
        back_dic = {'code': 1000, 'msg': ''} #给ajax做回调函数使用
        form_obj = myforms.MyRegForm(request.POST) #根据post请求携带的参数生成对象
        if form_obj.is_valid():
            clean_data = form_obj.cleaned_data #记录正确信息的大字典，form组件中的键值，不包括头像文件
            clean_data.pop('confirm_password') #不用保存确认密码
            file_obj = request.FILES.get('avatar') #拿到头像文件
            if file_obj:
                clean_data['avatar'] = file_obj
            models.UserInfo.objects.create_user(**clean_data)
            back_dic['url'] = '/login/'
        else:
            back_dic['code'] = 2000
            back_dic['msg'] = form_obj.errors
        return JsonResponse(back_dic)
    return render(request, 'register.html',locals())

def login(request):
    if request.method == 'POST':
        back_dic = {'code':1000, 'msg':''} #给前端ajax接收回调函数用
        username = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('code')
        if request.session.get('code').upper() == code.upper():
            user_obj = auth.authenticate(
                username = username,password=password
            ) #验证用户是否存在
            if user_obj:
                auth.login(request,user_obj) #保存用户的登录状态
                back_dic['url'] = '/home/' #登录成功后的跳转页面
            else:
                back_dic['code'] = 2000
                back_dic['msg'] = '用户名或密码错误'
        else:
            back_dic['code'] = 3000
            back_dic['msg'] = '验证码错误'
        return JsonResponse(back_dic) #返回json格式给ajax
    return render(request, 'login.html')




from PIL import Image, ImageDraw,ImageFont
import random
from io import BytesIO,StringIO

"""
BytesIO, 能够存储数据 并以二进制的格式再返回给你
StringIO， 能够存储数据 并以字符串的格式再返回给你
"""
"""
Image, 产生图片的
ImageDraw， 产生画笔的
ImageFont， 控制字体样式
"""
def get_random(): #三原色的数字随机生成
    return random.randint(0, 255),random.randint(0, 255),random.randint(0,255)

def get_code(request):
    img_obj = Image.new('RGB',(310,35),get_random()) #生成背景，包括颜色和尺寸
    img_draw = ImageDraw.Draw(img_obj) #生成图片的画笔对象
    img_font = ImageFont.truetype('static/font/2.otf', 40)  #生成字体样式及大小

    code=''
    for i in range(5):
        random_upper = chr(random.randint(65,90)) #大写字母
        random_lower = chr(random.randint(97,122)) #小写字母
        random_int = str(random.randint(0,9)) #数字类型
        temp = random.choice([random_upper,random_lower, random_int]) #随机选择上述三种类型的一种

        img_draw.text((i*45+45,-5),temp,get_random(),img_font) #用画笔把随机验证信息写进去（位置，数据，颜色，字体设置）
        code += temp #把验证码保存下来，用于后端手动验证
    print(code)
    request.session['code'] = code #验证码保存到session，用于后期的函数使用

    io_obj = BytesIO() #生成二进制对象
    img_obj.save(io_obj, 'png') #把画好二维码的背景图片以二进制流形式存成png格式
    return HttpResponse(io_obj.getvalue()) #存好之后数据返回前端
