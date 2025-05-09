"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from project import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # 后台基础
    path('system/', include('system.urls')),
    path('base/', include('base.urls')),
    path('shop/', include('shop.urls')),
    path('order/', include('order.urls')),
    path('barber/', include('barber.urls')),
    path('boss/', include('boss.urls')),
    path('activity/', include('activity.urls')),
    path('help/', include('help.urls')),
    path('user/', include('user.urls')),
    path('task/', include('task.urls')),
    path('coupon/', include('coupon.urls')),
    path('article/', include('article.urls')),
    path('member/', include('member.urls')),
    path('sample/', include('sample.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
