1 安装django

2 安装south：
south是一个django的数据库迁徙模块，使用south可以在程序的model发生改变的时候方便的自动对数据库进行修改
安装方法：easy_install south
官方网站：south.aeracode.org/

3 配置settings.py
在代码的根目录下新建名为settings.py的文件，将如下内容复制到文件里,并将$开头的变量替换为相应的值
# Django settings for myactivity project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('$user', '$email'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '$sqlname',                      # Or path to database file if using sqlite3.
        'USER': '$sqluser',                      # Not used with sqlite3.
        'PASSWORD': '$password',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

LOGIN_REDIRECT_URL = '/home/'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

SITE_ROOT = '$siteroot'

SITE_URL = '$siteurl'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = SITE_ROOT + 'media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

EMAIL_USE_TLS = True
EMAIL_HOST = '$smtphost'
EMAIL_HOST_USER = '$smptuser'
EMAIL_HOST_PASSWORD = '$smtppassword'
EMAIL_PORT = 587


# Make this unique, and don't share it with anybody.
SECRET_KEY = '*vun&2fyd(1s8kzxp7m6^xp55no8oa+q(2f(@ejprt8*)^s646'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    
)

INTERNAL_IPS = ('127.0.0.1',)

ROOT_URLCONF = 'myactivity.urls'

AUTH_PROFILE_MODULE = 'profile.Profile'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    SITE_ROOT + 'templates',
    
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'user_activity',
    'profile',
    'friends',
    'privacy',
    'story',
    'south',
    'message',
    'djcelery',
    'debug_toolbar',
    
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

import djcelery
djcelery.setup_loader()

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "$brokeruser"
BROKER_PASSWORD = "$brokerpassword"
BROKER_VHOST = "myactivity"
#CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("user_activity.manager", )

CELERYBEAT_SCHEDULE = {
    "runs-every-5-seconds": {
        "task": "user_activity.manager.change_state",
        "schedule": 60,
    },
}

4 安装djcelery
djcelery是用于执行定时和周期性任务，比如检查更新活动状态功能。
可以用easy_install djcelery 命令安装，如果只是建立测试服务器可以不开启，请跳过以下内容，但是必须安装网站才能运行。
安装配置rabbitmq

5 安装django-debug-toolbar
django-debug-toolbar是用于django程序调试的插件
安装方法：easy_install django-debug-toolbar

6配置数据库
在根目录下运行 python manage.py syncdb




