from django.shortcuts import render
from django.views.generic import View
from goods.models import *

class IndexView(View):
    def get(self,request):
        #获取商品的种类信息
        goodstype_list=GoodType.objects.all()
        #准备数据字典
        context={'goodstype_list':goodstype_list}

        return render(request,'goods/test_index.html',context)
