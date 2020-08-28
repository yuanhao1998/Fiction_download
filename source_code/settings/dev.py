import datetime
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

sys.path.insert(0, os.path.dirname(BASE_DIR) + os.sep + 'apps')

SECRET_KEY = 'g_*@^)u-3ll9sqw5-pwflh&_2ev+2@f3z)y=iyo#qi9x+zym_z'

DEBUG = True

ALLOWED_HOSTS = ['*']

# 指明自定义的用户模型类
AUTH_USER_MODEL = 'user.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',  # cors跨域
    'rest_framework',  # DRF

    'user',
    'bookshelves',
    'book',
    'hot',
    'search',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # csrf验证
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # cors跨域
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'source_code.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'source_code.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'cdb-dcn8l0ek.cd.tencentcdb.com',
        'PORT': 10172,
        'USER': 'root',
        'PASSWORD': 'yuan123hao',
        'NAME': 'Fiction'
    }
}

CACHES = {
    "default": {  # 默认存储信息: 存到 0 号库
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:yuan123hao@175.24.100.78:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {  # session 信息: 存到 1 号库
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:yuan123hao@175.24.100.78/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/fiction_web.log'),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}

# CORS跨域请求白名单设置
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
)
CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie

# DRF认证优先级配置
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',  # token认证
        # 'rest_framework.authentication.SessionAuthentication',  # session认证
        # 'rest_framework.authentication.BasicAuthentication',  # 基本认证
    ),
}
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    # 'JWT_RESPONSE_PAYLOAD_HANDLER': 'utils.JWTReturn.jwt_response_payload_handler',
}


LANGUAGE_CODE = 'zh-hans'  # 配置语言

TIME_ZONE = 'Asia/Shanghai'  # 配置时区

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = '/static/'
