from django.conf.urls import url
from django.contrib import admin

from projetos import views

urlpatterns = [    
    url(r'^grafico/$', views.viewGrafico ),
] 
