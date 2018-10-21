
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/',include('user.urls',namespace='user')),#user
    url(r'^tinymce/', include('tinymce.urls')),#tinymce

    url(r'^goods/',include('goods.urls',namespace='goods')),#user
]
