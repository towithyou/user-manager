from django.contrib import admin
from .models import CasBinPermissionRule, Role, \
    RoleBind, RouterView, RouterMeta

# Register your models here.


# class CasBinRuleAdmin(admin.ModelAdmin):
#     list_display = [
#         "id",
#         'ptype',
#         'v0',
#         'v1',
#         'v2',
#         'cid',
#         'v3',
#         'v4',
#     ]
#
#     search_fields = ('ptype', 'v0', 'v1')


class PermissionRuleAdmin(admin.ModelAdmin):
    list_display = ["ptype", "role", "path", "method", "cid"]

    search_fields = ('ptype', "role")


class RoleAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "alias", "remarks", "rid"]


class RoleBindAdmin(admin.ModelAdmin):
    list_display = ["ptype", "username", "role", "bid"]


class RouterViewAdmin(admin.ModelAdmin):
    list_display = ["path", "name", "component", "parent", "isParent"]


class RouterMetaAdmin(admin.ModelAdmin):
    list_display = ["title", "icon", "affix", "noCache", "breadcrumb"]


# admin.site.register(CasBinRule, CasBinRuleAdmin)
admin.site.register(CasBinPermissionRule, PermissionRuleAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(RoleBind, RoleBindAdmin)
admin.site.register(RouterView, RouterViewAdmin)
admin.site.register(RouterMeta, RouterMetaAdmin)


