from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import UserProfile

from django.contrib.auth.models import Group


class UserProfileAdmin(UserAdmin):
    # 显示部分
    list_display = [
        "uid",
        "username",
        "email",
        "department",
        "phone",
        "introduction",
        "is_active",
        "is_superuser",
        # "password"
    ]

    # 编辑布局
    fieldsets = (
        (_('个人信息'), {
            'fields': ('uid', 'username', 'phone', 'department',
                       'introduction', 'email', 'password',)
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'role'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.unregister(Group)   # 去掉组和权限