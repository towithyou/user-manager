from django_mysql.models import JSONField
from django.db import models
import uuid


# 角色
class Role(models.Model):
    name = models.CharField(max_length=32, verbose_name="角色")
    alias = models.CharField(max_length=32, verbose_name="别名")
    remarks = models.CharField(max_length=256, verbose_name="备注")
    rid = models.CharField(max_length=64, default=uuid.uuid4, verbose_name="rid")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'casbin_role'
        verbose_name_plural = verbose_name = '角色'
        unique_together = ("name", )


# 权限规则
class CasBinPermissionRule(models.Model):
    ptype = models.CharField(max_length=1, default="p", verbose_name="权限类型")
    role = models.CharField(max_length=128, verbose_name="角色")   # 手动创建关联
    path = models.CharField(max_length=128, verbose_name="api路径")
    method = models.CharField(max_length=128, verbose_name="请求方法")
    cid = models.CharField(max_length=64, default=uuid.uuid4, verbose_name="cid")
    v3 = models.CharField(max_length=32, null=True, blank=True)
    v4 = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return "{}-{}".format(self.ptype, self.role)

    def adapter(self):
        return {
            "ptype": self.ptype,
            "role": self.role,
            "path": self.path,
            "method": self.method,
        }

    class Meta:
        db_table = 'casbin_permission_rule'
        verbose_name_plural = verbose_name = '权限规则'
        unique_together = ('role', 'path', 'method')  # 联合唯一


# 角色绑定
class RoleBind(models.Model):
    ptype = models.CharField(max_length=1, default="g", verbose_name="权限类型")
    username = models.CharField(max_length=32, verbose_name="用户名")   # 手动创建关联
    role = models.CharField(max_length=32, verbose_name="角色")  # 手动创建关联
    bid = models.CharField(max_length=64, default=uuid.uuid4, verbose_name="bid")

    def __str__(self):
        return "{}-{}".format(self.ptype, self.role)

    def adapter(self):
        return {
            "ptype": self.ptype,
            "username": self.username,
            "role": self.role,
        }

    class Meta:
        db_table = 'casbin_role_bind'
        verbose_name_plural = verbose_name = '角色绑定'
        unique_together = ("username", "role")


class RouterMeta(models.Model):
    title = models.CharField(max_length=64, verbose_name="标题")
    icon = models.CharField(max_length=128, verbose_name="图表")
    affix = models.BooleanField(default=False, verbose_name="固定")
    noCache = models.BooleanField(default=True, verbose_name="关闭缓存")
    breadcrumb = models.BooleanField(default=True, verbose_name="面包屑中显示")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'router_meta'
        verbose_name_plural = verbose_name = '前端路由元数据'


class RouterView(models.Model):
    router_id = models.CharField(max_length=64, default=uuid.uuid4, verbose_name="路由ID")
    alias = models.CharField(max_length=64, default="", verbose_name="中文名")
    path = models.CharField(max_length=128, verbose_name="url路径")
    name = models.CharField(max_length=64, verbose_name="路由名称")
    component = models.CharField(max_length=512, verbose_name="组件路径")
    redirect = models.CharField(max_length=512, verbose_name="重定向路径", default="", blank=True)
    hidden = models.BooleanField(verbose_name="是否隐藏", default=False)
    parent = models.ForeignKey('self', null=True, blank=True, verbose_name="父路由", on_delete=models.CASCADE)
    role = models.ManyToManyField(to=Role, related_name="router_view",
                                  blank=True, verbose_name="角色")
    isParent = models.BooleanField(verbose_name="是否顶级路由")
    meta = models.OneToOneField(to=RouterMeta, on_delete=models.CASCADE)
    remarks = models.CharField(verbose_name="备注", max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'router_view'
        verbose_name_plural = verbose_name = '前端路由'


# Demo 弃用
# class CasBinRule(models.Model):
#     CHOICE_PTYPE = (
#         ('p', 'p'),
#         ('g', 'g'),
#     )
#     ptype = models.CharField(max_length=1, choices=CHOICE_PTYPE, verbose_name="p | g")
#     v0 = models.CharField(max_length=32, verbose_name="用户组 | 用户")
#     v1 = models.CharField(max_length=32, verbose_name="PATH | 用户组")
#     v2 = models.CharField(max_length=32, null=True, blank=True, verbose_name="METHOD")
#     cid = models.CharField(max_length=64, default=uuid.uuid4, verbose_name="cid")
#     v3 = models.CharField(max_length=32, null=True, blank=True)
#     v4 = models.CharField(max_length=32, null=True, blank=True)
#
#     def __str__(self):
#         return "{}-{}".format(self.ptype, self.v0)
#
#     class Meta:
#         db_table = 'casbin_rule'
#         verbose_name_plural = verbose_name = '权限系统<弃用>'
#
#     def serializer(self):
#         return {
#             'id': self.id,
#             'ptype': self.ptype,
#             'v0': self.v0,
#             'v1': self.v1,
#             'v2': self.v2,
#             'cid': self.cid,
#             'v3': self.v3,
#             'v4': self.v4,
#         }
#
#     def adapter(self):
#         return {
#             'ptype': self.ptype,
#             'v0': self.v0,
#             'v1': self.v1,
#             'v2': self.v2
#         }
