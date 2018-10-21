
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



SECRET_KEY = '-t(zs(&$td9@s6zrd!hkr-t$uzmiiqy5)xgj$4af7y08a2^3nu'


DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'user',
    'goods',
    'tinymce',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'daily_fresh.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #设置模板路径
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'daily_fresh.wsgi.application'




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'daily_fresh',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '192.168.12.202',
        'PORT': '3306',
    }
}

#设置时区、语言
LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#配置静态文件
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


#上传文件存储的路径
MEDIA_ROOT=os.path.join(BASE_DIR,"static/media")

#设置验证码字体
FONT_STYLE='/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf'

# 配置django认证系统使用的模型类
AUTH_USER_MODEL='user.User'

#配置发送邮件
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.163.com'#SMTP服务器
EMAIL_PORT=25#端口号
EMAIL_HOST_USER='15039961137@163.COM'#发送邮件的邮箱
EMAIL_HOST_PASSWORD='python1807'#在邮箱中设置的客户端授权密码
EMAIL_FROM='天天生鲜<15039961137@163.com>'#收件人看到的发件人


#配置登录url
LOGIN_URL='/user/login'


#上传文件存储的路径
# MEDIA_ROOT=os.path.join(BASE_DIR,"static/media")


#sessin 交给redis管理
SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_HOST = 'localhost'
SESSION_REDIS_PORT = 6379
SESSION_REDIS_DB = 1
SESSION_REDIS_PASSWORD = ''
SESSION_REDIS_PREFIX = 'session'

#配置tinymce
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',
    'width': 600,
    'height': 400,
}

#FastDFS设置-自定义存储的类
DEFAULT_FILE_STORAGE='utils.fdfs.storage_util.FDFSStorage'
#FastDFS设置-客户端配置文件
FDFS_CLIENT_CONF='utils/fdfs/client.conf'
#FastDFS设置-url
FDFS_URL='http://%s:9999/'%('192.168.12.202')