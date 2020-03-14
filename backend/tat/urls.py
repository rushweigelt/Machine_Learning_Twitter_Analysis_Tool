"""tat URL Configuration

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
from django.urls import path, re_path, include

from . import views

#app_name = 'tat'
urlpatterns = [
    path('heatmap/', views.heatmap, name='heatmap'),
    path('purpose/', views.purpose, name='purpose'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    #path('', views.index, name='index'),
    path('api/', views.HashtagSearchCreate.as_view()),
    path('', include('frontend.urls')),
    #path('', views.index.as_view()),
    #path('admin/', admin.site.urls),
    #re_path(r'', views.catchall),
]
