from django.urls import path
from .v1 import views

urlpatterns = [
    path('v1/router/', views.Router.as_view()),
    path('v1/role/', views.RoleView.as_view(
        {
            "get": "list",
            "post": 'create'
        }
    )),
    path('v1/role/<str:rid>/', views.RoleView.as_view(
        {
            "get": "retrieve",
            "put": "update",
            "delete": "destroy",
        }
    )),

    # 角色反向关联
    path('v1/role-related/<str:rid>/', views.RoleRelated.as_view()),

    path('v1/permission/', views.PermissionRuleView.as_view(
        {
            "get": "list",
            "post": 'create'
        }
    )),
    path('v1/permission/<str:cid>/', views.PermissionRuleView.as_view(
        {
            "get": "retrieve",
            "put": "update",
            "delete": "destroy",
        }
    )),

    path('v1/role-bind/', views.PermissionRoleBindView.as_view(
        {
            "get": "list",
            "post": 'create'
        }
    )),
    path('v1/role-bind/<str:bid>/', views.PermissionRoleBindView.as_view(
        {
            "get": "retrieve",
            "put": "update",
            "delete": "destroy",
        }
    )),

    # 前端路由管理
    path('v1/router-manager/', views.RouterManager.as_view(
        {
            "get": "list",
            "post": 'create'
        }
    )),
    # 前端路由管理
    path('v1/router-manager/<str:router_id>/', views.RouterManager.as_view(
        {
            "get": "retrieve",
            "put": 'update',
            "delete": 'destroy',
        }
    )),
]
