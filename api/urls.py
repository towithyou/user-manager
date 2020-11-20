from django.urls import path
from . import views

urlpatterns = [
    path('v1/host/', views.HostView.as_view()),
    path('v1/dns/', views.DNSView.as_view())
]
