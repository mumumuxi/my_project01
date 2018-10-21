from django.contrib import admin
from goods.models import *

admin.site.register(GoodType)
admin.site.register(Goods)
admin.site.register(GoodsSKU)
admin.site.register(GoodsImage)