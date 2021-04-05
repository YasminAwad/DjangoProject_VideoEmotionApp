"""progetto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from app1 import views

urlpatterns = [
   path('admin/', admin.site.urls),
   path('',views.start, name= "start"),
   path( 'home',views.home, name= "homeview"),
   path('<int:pk>',views.videoDet, name= "video"),
   path('emotion',views.emotion, name= "emotion"),
   path('emotionReading',views.emotionReading, name= "emotionReading"),
   path('saveData',views.saveData, name= "saveData"),
   path('<int:pk>/getData',views.getData, name= "getData"),
   path('<int:pk>/statistics',views.getStat, name= "statistics"),
   path('saveStat',views.saveStat, name= "stat"),
]
