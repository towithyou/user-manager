"""user_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

from api import urls as api_urls
from users import urls as users_urls
from permission import urls as perm_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),  # api 测试
    path('api/', include(users_urls)),  # 用户
    path('api/', include(perm_urls)),   # 权限
    path('api-token-auth/', obtain_jwt_token),  # 请求颁发token
    path('api-token-verify/', verify_jwt_token),  # 验证token 是否过期
]
