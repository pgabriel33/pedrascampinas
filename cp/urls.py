"""cp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.__home, name='__home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='__home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as v
from users.views import user_login
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	path('',views.home,name='home'),
    path('accounts/login/', user_login, name='login'),
    path('login/', user_login, name='login'),
    path('accounts/logout/', v.logout_then_login, name='logout'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('produtos/', include('products.urls')),    
]
if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)