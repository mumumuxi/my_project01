from django.db import models

from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel


class User(AbstractUser,BaseModel):

    # 用户模型类
    class Meta:
        db_table = 'userinfo'
        verbose_name='用户'
        verbose_name_plural=verbose_name

class Province(models.Model):
    pname = models.CharField(max_length=100)
    def __str__(self):
        return self.pname


class City(models.Model):
    cname = models.CharField(max_length=100)
    cprovince=models.ForeignKey(Province)
    def __str__(self):
        return self.cname

class Area(models.Model):
    aname = models.CharField(max_length=100)
    acity=models.ForeignKey(City)
    def __str__(self):
        return self.aname

class Address(BaseModel): # BaseModel 自己写的utils.models下，继承了记录时间字段
    """
    用户的收货地址
    """
    # 关联等级：CASCADE　表示主键被删除了，则外键对应的数据也被删除，级联删除
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    # 关联等级：PROTECT 表示主键删除的时候，必须外键先被删除，保护
    province = models.ForeignKey('Province', on_delete=models.PROTECT, related_name='province_addresses', verbose_name='省')
    city = models.ForeignKey('City', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('Area', on_delete=models.PROTECT, related_name='district_addresses', verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    postcode=models.CharField(max_length=6,verbose_name='邮政编码')
    is_default=models.BooleanField(default=False,verbose_name='是否设为默认')

    class Meta:
        db_table = 'address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name