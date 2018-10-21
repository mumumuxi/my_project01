
from django.conf.urls import include, url
from django.contrib import admin
from user import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^index$', views.index,name='index'),
    url(r'^register$', views.RedisterView.as_view(),name='register'),#注册
    url(r'^user_name_exist$', views.user_name_exist,name='user_name_exist'),#异步判断用户名是否存在

    url(r'^active/(?P<token>.*)$', views.ActiveView.as_view(),name='active'),#账户激活

    url(r'^login$', views.LoginView.as_view(),name='login'),#登录
    url(r'^validate_code$', views.validate_code, name='validate_code'),#验证码

    url(r'^logout_view$', views.logout_view, name='logout_view'),  # 注销/退出

    url(r'^userinfo$', views.UserInfoView.as_view(),name='userinfo'),#用户中心——信息页
    url(r'^order$', views.UserOrderView.as_view(),name='order'),#用户中心——订单页
    url(r'^address$', views.UserAddressView.as_view(),name='address'),#用户中心——地址页

    # url(r'^$', login_required(views.UserInfoView.as_view()),name='userinfo'),#用户中心——信息页
    # url(r'^order$', login_required(views.UserOrderView.as_view()),name='order'),#用户中心——订单页
    # url(r'^address$', login_required(views.UserAddressView.as_view()),name='address$'),#用户中心——地址页



    url(r'^forget_pwd$', views.forget_pwd,name='forget_pwd'),#忘记密码
    url(r'^success_send$', views.success_send,name='success_send'),#成功发送邮件
    url(r'^pwd_reset/(?P<token>.*)$', views.pwd_reset,name='pwd_reset'),#重置密码
    url(r'^pwd_reset_handler$', views.pwd_reset_handle,name='pwd_reset_handle'),#重置密码


    url(r'^get_all_province$', views.get_all_province, name='get_all_province'),#三级联动
    url(r'^get_city_by_pid$', views.get_city_by_pid, name='get_city_by_pid'),
    url(r'^get_area_by_cid$', views.get_area_by_cid, name='get_area_by_cid'),



]
