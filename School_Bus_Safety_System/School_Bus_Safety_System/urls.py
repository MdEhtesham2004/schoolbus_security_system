"""
URL configuration for School_Bus_Safety_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),   
    path('home',views.home,name='homepage'),   
    path('index',views.index,name='index'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('admin_previlages',views.show_admin_previlages,name='admin_previlages'),
    path('register_student',views.register_student,name='register_student'),
    path('parents_view',views.show_parents_view,name='parents_view'),
    path('logout',views.logout, name='logout'),
    path('mylocation/', views.mylocation_view, name='mylocation'),
    path('admin_login', views.admin_login, name='admin_login'),

    #
]
