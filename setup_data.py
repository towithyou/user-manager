import os
import sys
import logging


formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
s_handler = logging.StreamHandler()
s_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(s_handler)


def setup():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'user_manager.settings')
    import django
    django.setup()


def init_admin_user(role_obj):
    from users.models import UserProfile
    default_admin_username = "admin"
    default_admin_password = "admin"

    user = UserProfile.objects.all().filter(username__exact=default_admin_username)
    if user:
        logger.error("<admin>用户已创建")
        ret_user = user[0]
    else:
        info = {
            "username": default_admin_username,
            "email": 'admin@qq.com',
            "phone": "13888888888",
            "department": "管理员",
            "is_active": True,
            "is_superuser": True,
            "is_staff": True,
        }
        u = UserProfile.objects.create(**info)
        us = UserProfile.objects.get(username__exact=default_admin_username)
        us.set_password(default_admin_password)
        us.role.add(role_obj.id)
        us.save()
        ret_user = us
        logger.info("<{}>用户创建成功".format(u.username))

    return ret_user


def init_admin_role():
    from permission.models import Role
    from django.conf import settings
    admin_role = settings.ADMIN_ROLE

    role = Role.objects.all().filter(name__exact=admin_role)
    if role:
        logger.error("<{}>角色已经创建".format(role[0].name))
        ret_role = role[0]
    else:
        r = Role.objects.create(**{"name": admin_role, "alias": "管理员", "remarks": "管理员角色"})
        logger.info("<{}>角色创建成功".format(r.name))
        ret_role = r

    return ret_role


def init_permission():
    from permission.models import CasBinPermissionRule
    from django.conf import settings
    admin_role = settings.ADMIN_ROLE

    pr = CasBinPermissionRule.objects.all().filter(role__exact=admin_role)
    if pr:
        logger.error("<admin>权限已经创建")
    else:
        perm = CasBinPermissionRule.objects.create(**{
            "ptype": "p",
            "role": admin_role,
            "path": "*",
            "method": "*",
        })
        logger.info("<{}>权限创建成功".format(perm.role))


def init_role_bind():
    from permission.models import RoleBind
    from django.conf import settings
    admin_role = settings.ADMIN_ROLE

    rb = RoleBind.objects.all().filter(username__exact="admin", role__exact=admin_role)
    if rb:
        logger.error("<admin>角色绑定已经创建")
    else:
        bind = RoleBind.objects.create(**{
            "ptype": "g",
            "username": "admin",
            "role": admin_role,
        })
        logger.info("<{}-{}>权限创建成功".format(bind.username, bind.role))


def init_router_view():
    from permission.models import RouterView, RouterMeta
    qs = RouterView.objects.all()
    if qs:
        logger.error("前端路由已创建, 如果显示不全，请删除数据库重新执行脚本")
        return
    # ecs 主机 视图
    h1 = {
        "alias": "主机管理",
        "path": "/host",
        "name": "hostManager",
        "component": "layout/index",
        "redirect": "/host/index",
        "isParent": True,
        "remarks": "主机管理备注",
        "parent": None
    }
    m1 = {
        "title": "主机管理",
        "icon": "el-icon-monitor",
    }
    h1 = RouterView(**h1)
    m1 = RouterMeta.objects.create(**m1)
    h1.meta = m1
    h1.save()
    logger.info("{}路由创建成功".format(h1.alias))

    h2 = {
        "alias": "主机信息",
        "path": "index",
        "name": "hostIndex",
        "component": "views/host/index",
        "isParent": False,
        "remarks": "主机备注",
    }
    m2 = {
        "title": "主机管理",
        "icon": "el-icon-monitor",
    }
    h2 = RouterView(**h2)
    m2 = RouterMeta.objects.create(**m2)
    h2.parent = h1
    h2.meta = m2
    h2.save()
    logger.info("{}路由创建成功".format(h2.alias))

    # dns 视图
    d1 = {
        "alias": "DNS管理",
        "path": "/dns",
        "name": "dnsBase",
        "component": "layout/index",
        "redirect": "/dns/index",
        "hidden": False,
        "isParent": True,
        "remarks": "DNS管理",
        "parent": None,
    }
    md1 = {
        "title": "DNS管理",
        "icon": "chart",
    }
    d1 = RouterView(**d1)
    md1 = RouterMeta.objects.create(**md1)
    d1.meta = md1
    d1.save()
    logger.info("{}路由创建成功".format(d1.alias))

    d2 = {
        "alias": "DNS信息",
        "path": "index",
        "name": "dnsIndex",
        "component": "views/dns/index",
        "isParent": False,
        "remarks": "主机备注",
    }
    md2 = {
        "title": "DNS信息",
        "icon": "el-icon-help",
    }
    d2 = RouterView(**d2)
    md2 = RouterMeta.objects.create(**md2)
    d2.parent = d1
    d2.meta = md2
    d2.save()
    logger.info("{}路由创建成功".format(d2.alias))

    # keyboard view
    k1 = {
        "alias": "键盘图表layout",
        "path": "/keyboard",
        "name": "keyboard",
        "component": "layout/index",
        "redirect": "/keyboard/index",
        "isParent": True,
        "parent": None
    }
    kd1 = {
        "title": "键盘图表",
        "icon": "el-icon-s-grid",
    }
    k1 = RouterView(**k1)
    kd1 = RouterMeta.objects.create(**kd1)
    k1.meta = kd1
    k1.save()
    logger.info("{}路由创建成功".format(k1.alias))

    k2 = {
        "alias": "键盘图表",
        "path": "index",
        "name": "testIndex",
        "component": "views/Chart",
        "isParent": False,
        "remarks": "键盘",
    }
    kd2 = {
        "title": "键盘图表",
        "icon": "el-icon-s-grid",
    }
    k2 = RouterView(**k2)
    kd2 = RouterMeta.objects.create(**kd2)
    k2.meta = kd2
    k2.parent = k1
    k2.save()
    logger.info("{}路由创建成功".format(k2.alias))

    # 日历 view
    date1 = {
        "alias": "日历",
        "path": "/calendar",
        "name": "calendar",
        "component": "layout/index",
        "redirect": "/calendar/index/",
        "isParent": True,
        "remarks": "日历",
        "parent": None,
    }
    data1_m = {
        "title": "日历",
        "icon": "el-icon-date",
    }
    date1 = RouterView(**date1)
    data1_m = RouterMeta.objects.create(**data1_m)
    date1.meta = data1_m
    date1.save()
    logger.info("{}路由创建成功".format(date1.alias))

    date2 = {
        "alias": "日历",
        "path": "index",
        "name": "dateIndex",
        "component": "views/Date",
        "redirect": "",
        "isParent": False,
        "remarks": "el-icon-date",
    }
    data2_m = {
        "title": "日历",
        "icon": "el-icon-date",
    }
    date2 = RouterView(**date2)
    data2_m = RouterMeta.objects.create(**data2_m)
    date2.meta = data2_m
    date2.parent = date1
    date2.save()
    logger.info("{}路由创建成功".format(date2.alias))

    # error page
    ep1 = {
        "alias": "错误页面",
        "path": "/error-page",
        "name": "errorPage",
        "component": "layout/index",
        "redirect": "/error-page/index",
        "isParent": True,
        "remarks": "el-icon-warning",
        "parent": None,
    }
    epm1 = {
        "title": "错误页面",
        "icon": "el-icon-warning",
    }
    ep1 = RouterView(**ep1)
    epm1 = RouterMeta.objects.create(**epm1)
    ep1.meta = epm1
    ep1.save()
    logger.info("{}路由创建成功".format(ep1.alias))

    ep2 = {
        "alias": "错误页面测试",
        "path": "index",
        "name": "errorPageIndex",
        "component": "views/ErrorPage",
        "isParent": False,
        "remarks": "错误页面测试",
    }
    epm2 = {
        "title": "错误页面",
        "icon": "el-icon-warning",
    }
    ep2 = RouterView(**ep2)
    epm2 = RouterMeta.objects.create(**epm2)
    ep2.meta = epm2
    ep2.parent = ep1
    ep2.save()
    logger.info("{}路由创建成功".format(ep2.alias))


if __name__ == '__main__':
    setup()
    # 创建admin 角色
    ins = init_admin_role()
    # 创建用户
    init_admin_user(ins)
    # 创建权限
    init_permission()
    # 用户权限绑定
    init_role_bind()
    # 前端视图
    init_router_view()
