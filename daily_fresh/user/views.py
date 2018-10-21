from django.shortcuts import render,redirect
from django.conf import settings
from  user.models import *
from utils import my_md5
from django.http import HttpResponse,JsonResponse
import json
import re
from django.core.urlresolvers import reverse
# 引入绘图模块
from PIL import Image,ImageDraw,ImageFont
import random
from io import BytesIO
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,SignatureExpired,BadSignature
from daily_fresh import settings
from django.views.generic import View
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from my_celery.celery_tasks import tasks_send_mail
from utils.user_utils import LoginRequiredMixin
from django.core import serializers




def index(request):
    user_name = request.session.get('user_name')
    context = {
               'user_name': user_name,
               }
    return render(request,'user/index.html',context)

class RedisterView(View):
    def get(self,request):
        # 注册页面
        return render(request, 'user/register.html')

    def post(self,request):
        '''注册处理'''
        # 获取属性
        user_name = request.POST.get('user_name', '').strip()
        pwd = request.POST.get('pwd', '').strip()
        cpwd = request.POST.get('cpwd', '').strip()
        email = request.POST.get('email', '').strip()
        allow = request.POST.get('allow')

        # 判断数据完整性
        if not all([user_name, pwd, email, cpwd, allow]):
            return render(request, 'user/register.html', {'errors': '请完善您的信息！'})

        # 校验两次输入的密码是否相同
        if cpwd != pwd:
            return render(request, 'user/register.html', {'errors': '密码输入不一致！！'})

        # 检验邮箱
        if not re.match('^[.a-zA-Z0-9_-]\w{4,20}@(163|qq|126)\.com$', email):
            return render(request, 'user/register.html', {'errors': '邮箱格式不正确！'})

        # 校验用户名是否重复
        if User.objects.filter(username=user_name):
            return render(request, 'user/register.html', {'errors': '用户名重复！'})

        if user_name == '':
            return render(request, 'user/register.html', {'errors': '用户名不能为空！'})

        # try:
        #     user=User.objects.get(username=user_name)
        # except user.DoesNotExist:
        #     # 用户名不存在
        #     user=None
        # if user:
        #     return render(request, 'user/register', {'errors': '用户名重复！'})

        # 进行用户注册
        user = User.objects.create_user(user_name, email, pwd)
        user.is_active = 0
        user.save()

        '''
        发送邮件激活，包含激活链接：http://ip:port/user/cctive/3
        激活链接中需要包含用户的身份信息，并且要把身份信息进行加密
        '''

        # 加密用户的身份信息，生成激活token
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info).decode()
        encryption_url = 'http://192.168.12.202:2222/user/active/%s' % token

        # 发邮件
        subject = '天天生鲜欢迎信息'  # 主题
        message = ''  # 文本内容
        sender = settings.EMAIL_FROM  # 发件人
        receiver = [email]  # 收件人
        html_message = '<h1>%s,欢迎您成为天天生鲜的注册会员</h1>请点击下面的链接激活您的账户</br><a href="%s">%s</a>' % (
        user_name, encryption_url, encryption_url)

        # 发送邮件
        tasks_send_mail.delay(subject, message, sender, receiver, html_message)

        # 返回应答，跳转到登录界面
        return render(request, 'user/login.html')

 #异步处理：判断注册时用户户名是否存在
def user_name_exist(request):
    user_name = request.GET.get('user_name')
    count = User.objects.filter(username=user_name).count()  # [{'name': 'mouhuan'}]
    return JsonResponse({'count':count})


class ActiveView(View):
    '''用户激活'''
    def get(self,request,token):
        '''进行用户激活'''
        #进行解密，获取要激活的用户信息
        serializer=Serializer(settings.SECRET_KEY,3600)
        try:
            info=serializer.loads(token)
            #获取待激活用户的id
            user_id=info['confirm']

            #根据id获取用户信息
            user=User.objects.get(id=user_id)
            user.is_active=1
            user.save()

            #跳转到登陆界面
            return render(request, 'user/login.html')

        except SignatureExpired as e:
            #激活链接已过期
            return HttpResponse('激活链接已过期！')
        except BadSignature as e:
            #激活链接被修改
            return HttpResponse('激活链接非法！')



class LoginView(View):
    '''登录'''

    def get(self,request):
        '''显示登录界面'''

        #判断是否选择了记住用户名
        remeber_user_name = request.COOKIES.get('remeber_user_name', '')
        if remeber_user_name:
            return render(request, 'user/login.html', {'remeber_user_name': remeber_user_name})
        else:
            return render(request, 'user/login.html')

    def post(self,request):
        '''登录校验'''
        #接收数据
        user_name = request.POST.get('username')
        pwd = request.POST.get('pwd')
        validate = request.POST.get('validate')
        remember = request.POST.get('remember')

        user = authenticate(username=user_name, password=pwd)
        # 用户存在
        if user is not None:

            # 判断验证码是否正确
            if validate == request.session.get('validate_code').lower():

                # 验证是否激活
                if user.is_active:
                    #记录用户的登录状态
                    login(request, user)

                    #获取url后面的参数（next=xxxx），记录用户登录前访问的页面，登陆后跳转到访问页面
                    #虽然是post请求，但是要用get方法获取，因为是rl后面携带的参数
                    next_url=request.GET.get('next')
                    print(next_url)
                    if next_url:
                        resp= redirect(next_url)
                    else:
                        resp = redirect(reverse('user:index'))

                    #判断是否记住用户名
                    if remember != None:
                        resp.set_cookie('remeber_user_name', user_name, 3600 * 24 * 7)
                    else:
                        resp.set_cookie('remeber_user_name', user_name, 0)

                    # 将用户id和用户名保存在session中
                    # request.session['user_id'] = user[0].id
                    request.session['user_name']=user_name


                    return resp
                else:
                    # 用户未激活
                    return render(request, 'user/login.html', {'doNotActive': '您的账号还没有激活，请注意查收邮箱消息，进行激活'})
            else:
                return render(request, 'user/login.html', {'validate_error': '验证码错误'})

        else:
            # 用户不存在
            return render(request, 'user/login.html', {'doNotUser': '用户名或密码错误'})

def logout_view(request):
    # 退出登录，清除session
    logout(request)
    request.session.flush()
    return redirect(reverse('user:index'))



class UserInfoView(LoginRequiredMixin,View):
    '''用户中心——信息页'''

    def get(self,request):
        # 获取登录用户对应的user对象
        user = request.user

        # 获取用户的默认收货地址
        try:
            address = Address.objects.get(user=user, is_default=True)
        except Address.DoesNotExist:
            # 不存在默认收货地址
            address = None

        #从session中获取用户名
        user_name=request.session.get('user_name')
        context={'page':'1',
                 'user_name':user_name,
                 'address':address
                 }

        return render(request,'user/user_center_info.html',context)



class UserOrderView(LoginRequiredMixin,View):
    '''用户中心——订单页'''

    def get(self, request):
        user_name = request.session.get('user_name')
        context = {'page': '2',
                   'user_name': user_name
                   }
        return render(request, 'user/user_center_order.html', context)

def get_all_province(request):
    province_list=Province.objects.all()
    content={
        'province_list':serializers.serialize('json',province_list),
    }
    return JsonResponse(content)

def get_city_by_pid(request):
    province_id=request.GET.get('province_id')
    print(province_id)

    province=Province.objects.get(id=province_id)
    print(province)

    city_list=City.objects.filter(cprovince_id=province_id)
    content={
        'city_list':serializers.serialize('json',city_list)
    }
    return JsonResponse(content)

def get_area_by_cid(request):
    city_id=request.GET.get('city_id')

    city=City.objects.get(id=city_id)
    print(city)

    area_id = request.GET.get("area_id")
    print(area_id)

    area_list=Area.objects.filter(acity_id=city_id)
    print(area_list)

    content={
        'area_list':serializers.serialize('json',area_list)
    }
    return JsonResponse(content)

class UserAddressView(LoginRequiredMixin,View):
    '''用户中心——地址页'''

    def get(self, request):
        #获取登录用户对应的user对象
        user=request.user

        #获取用户的默认收货地址
        try:
            address=Address.objects.get(user=user,is_default=True)
        except Address.DoesNotExist:
            #不存在默认收货地址
            address=None
        #数据字典
        user_name = request.session.get('user_name')
        all_address=request.session.get('all_address')
        context = {'page': '3',
                   'user_name': user_name,
                   'address':address,
                   'all_address':all_address
                   }
        return render(request, 'user/user_center_site.html', context)

    def post(self,request):
        '''地址的添加'''

        #接收数据
        receiver=request.POST.get('receiver')
        place=request.POST.get('place')
        postcode=request.POST.get('postcode')
        mobile=request.POST.get('mobile')

        province_id = request.POST.get('province_id')
        try:
            province = Province.objects.get(id=province_id)
        except:
            province=None
        print(province)

        city_id = request.POST.get('city_id')
        try:
            city = City.objects.get(id=city_id)
        except:
            city=None
        print(city)

        area_id = request.POST.get('area_id')
        try:
            area = Area.objects.get(id=area_id)
        except:
            area=None
        print(area)

        # 数据字典
        user_name = request.session.get('user_name')
        # 获取登录用户对应的user对象
        user = request.user
        # 获取用户的默认收货地址
        try:
            address = Address.objects.get(user=user, is_default=True)
        except Address.DoesNotExist:
            address=None
        print(address)


        full_address=str(province)+str(city)+str(area)+str(place)
        print(full_address)



        if all([receiver,place,postcode,mobile,province,city,area]):
            request.session['all_address']= full_address


        all_address=request.session.get('all_address')
        print(all_address)



        #校验数据
        if not all([receiver,place,postcode,mobile,province,city,area]):
            return render(request,'user/user_center_site.html',{'page': '3','user_name': user_name,'all_address':all_address,'address': address,'errors':'信息不完整，请重新填写！'})

        #校验手机号
        if not re.match('^(13|15|17|18)\d{9}$',mobile):
            return render(request,'user/user_center_site.html',{'page': '3','user_name': user_name,'all_address':all_address,'address': address,'errors':'手机号码格式不正确，请重新填写！'})

        #校验邮政编码
        if not re.match('^[0-9]\w{5}',postcode):
            return render(request, 'user/user_center_site.html', {'page': '3','user_name': user_name,'all_address':all_address,'address': address,'errors': '邮政编码格式不正确，请重新填写！'})


        #业务处理，添加地址
        #用户添加的地址作为默认地址，如果原来有默认地址要取消
        #获取用户的默认收货地址

        # 获取登录用户对应的user对象
        user = request.user
        # 获取用户的默认收货地址
        try:
            address = Address.objects.get(user=user, is_default=True)
            address.is_default=False
            address.save()

        except Address.DoesNotExist:
            # 不存在默认收货地址
            pass

        #添加地址
        Address.objects.create(user=user,
                               province=province,
                               city=city,
                               district=area,
                               receiver=receiver,
                               postcode=postcode,
                               mobile=mobile,
                               place=place,
                               is_default=True)
        return redirect(reverse('user:address'))

def validate_code(request):
    #定义变量，用于画面的背景色，宽，高
    # bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    bgcolor=(255,255,255)
    width = 152
    height = 38
    # 创建画面对象
    img = Image.new('RGB', (width, height), bgcolor)

    # 创建画笔对象
    draw = ImageDraw.Draw(img)

    # 调用画笔的point()函数绘制噪点
    for i in range(0, 200):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        draw.point(xy, fill=fill)

    # 定义验证码的备选值
    str1 = 'abcd123efgh456ijklmn789opqr0stuvwxyzABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'

    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]

    # 保存到sesison
    request.session["validate_code"] = rand_str

    # 构造字体对象
    font = ImageFont.truetype(settings.FONT_STYLE, 33)
    # 绘制4个字
    for i in range(4):
        # 构造字体颜色
        fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
        draw.text((7 + 36 * i, 2), rand_str[i], font=font, fill=fontcolor)

    # 释放画笔
    del draw
    buf = BytesIO()

    # 将图片保存在内存中，文件类型为png
    img.save(buf, 'png')

    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


def forget_pwd(request):
    return render(request,'user/forget.html')


def success_send(request):
    #获取数据
    user_name=request.POST.get('user_name')
    email=request.POST.get('email')
    user=User.objects.filter(username=user_name)

    if user:
        if user[0].email!=email:
            return render(request,'user/forget.html',{'errors':'邮箱不匹配，请重新输入！'})
        else:

            '''
            发送邮件修改密码，包含修改链接：http://ip:port/user/pwd_reset/3
            链接中需要包含用户的身份信息，并且要把身份信息进行加密
            '''

            # 加密用户的身份信息，生成激活token
            serializer = Serializer(settings.SECRET_KEY, 3600)
            info = {'confirm': user[0].id}
            token = serializer.dumps(info).decode()
            encryption_url = 'http://192.168.12.202:2222/user/pwd_reset/%s' % token

            # 发邮件
            subject = '天天生鲜会员修改密码'  # 主题
            message = ''  # 文本内容
            sender = settings.EMAIL_FROM  # 发件人
            receiver = [email]  # 收件人
            html_message = '<h1>%s,你好呀，小迷糊</h1>请点击下面的链接修改您的账户密码</br><a href="%s">%s</a>'%(user_name, encryption_url, encryption_url)

            # 发送邮件
            send_mail(subject, message, sender, receiver, html_message=html_message)

            return render(request,'user/success_send.html')
    else:
        return render(request,'user/forget.html',{'errors':'用户名不存在，请重新输入！'})


def pwd_reset(request,token):
    '''进行用户修改密码'''
    serializer = Serializer(settings.SECRET_KEY, 3600)
    try:
        info = serializer.loads(token)
        token = serializer.dumps(info).decode()
        # 跳转到登陆界面
        return render(request, 'user/pwd_reset.html',{'path':token})
    except SignatureExpired as e:
        # 修改链接已过期
        return HttpResponse('修改密码链接已过期！')
    except BadSignature as e:
        # 修改链接被修改
        return HttpResponse('修改密码链接非法！')
def pwd_reset_handle(request):
    #获取数据
    newpwd1=request.POST.get('newpwd1')
    newpwd2 = request.POST.get('newpwd2')
    #获取url路径
    path=request.POST.get('path')
    # 进行解密，获取要激活的用户信息
    serializer = Serializer(settings.SECRET_KEY, 3600)
    info = serializer.loads(path)
    # 获取待修改用户的id
    user_id = info['confirm']

    # 根据id获取用户信息
    user = User.objects.get(id=user_id)
    if newpwd1==newpwd2:
        user.set_password(newpwd1)
        user.save()
        return redirect(reverse('user:login'))
    else:
        return render(request,'user/pwd_reset.html',{'errors':'两次输入的密码不一致，请重新输入！'})





