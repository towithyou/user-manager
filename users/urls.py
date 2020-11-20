from django.urls import path
from .v1 import views

urlpatterns = [
    path('v1/user/', views.UserView.as_view({
        "get": "list",
        "post": 'create'
    })),

    path('v1/user/<str:uid>/', views.UserView.as_view({
        "get": "retrieve",
        "patch": "update",
        "put": "update",
        "delete": "destroy",
    })),

    path('v1/user-profile/', views.UserInfo.as_view())

]
